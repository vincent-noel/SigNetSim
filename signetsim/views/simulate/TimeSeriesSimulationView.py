#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014-2017 Vincent Noel (vincent.noel@butantan.gov.br)
#
# This file is part of libSigNetSim.
#
# libSigNetSim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# libSigNetSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with libSigNetSim.  If not, see <http://www.gnu.org/licenses/>.

""" TimeSeriesSimulationView.py

	This file ...

"""

from django.views.generic import TemplateView
from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.views.simulate.SedmlWriter import SedmlWriter

from signetsim.views.simulate.TimeSeriesSimulationForm import TimeSeriesSimulationForm
from signetsim.models import Experiment, Condition, Treatment, SEDMLSimulation, new_sedml_filename
from signetsim.managers.data import buildExperiment
from signetsim.settings.Settings import Settings

from libsignetsim.simulation.TimeseriesSimulation import TimeseriesSimulation
from libsignetsim.LibSigNetSimException import LibSigNetSimException

from django.conf import settings
from django.core.files import File
from django.shortcuts import redirect

from os.path import basename, join


class TimeSeriesSimulationView(TemplateView, HasWorkingModel, SedmlWriter):

	template_name = 'simulate/timeseries.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)
		SedmlWriter.__init__(self)

		self.form = TimeSeriesSimulationForm(self)

		self.listOfVariables = None
		self.listOfReactions = None
		self.experiments = None
		self.nbConditions = None
		self.experimentName = None

		self.observations = None

		self.simResults = None
		self.t_unit = None
		self.y_unit = None
		self.y_max = 0

		self.experiment = None


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)

		kwargs['species'] = self.listOfVariables
		kwargs['reactions'] = self.listOfReactions
		kwargs['experiments'] = self.experiments

		if self.experiment is not None:
			kwargs['experiment_name'] = self.experiment.name
			kwargs['experiment_observations'] = [condition.listOfExperimentalData for condition in self.experiment.listOfConditions.values()]

		kwargs['ids_species_selected'] = self.form.selectedSpeciesIds
		kwargs['ids_reactions_selected'] = self.form.selectedReactionsIds

		kwargs['sim_results'] = self.simResults
		kwargs['t_unit'] = self.t_unit
		kwargs['y_unit'] = self.y_unit
		kwargs['y_max'] = self.y_max
		kwargs['colors'] = Settings.default_colors

		# kwargs['simulation_results_loaded'] = self.simulationResultsLoaded

		kwargs['form'] = self.form
		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingModel.isChooseModel(self, request):
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "simulate_model":
				self.simulateModel(request)

			elif request.POST['action'] == "save_simulation":
				self.saveSimulation(request)
				redirect('list_of_simulations')

		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.loadVariables()
			self.loadReactions()
			self.loadExperiments(request)

	def read_timeseries(self, results):

		# generating results
		self.simResults = []
		for i, result in enumerate(results):
			(t_t, t_y) = result

			y_filtered = {}
			if self.form.selectedSpeciesIds is not None:
				for var in self.form.selectedSpeciesIds:
					t_sbml_id = self.listOfVariables[var].getSbmlId()
					t_name = self.listOfVariables[var].getNameOrSbmlId()
					if self.form.showObservations == True:
						t_name += " (model)"
					y_filtered.update({t_name: t_y[t_sbml_id]})

			if self.form.selectedReactionsIds is not None:
				for var in self.form.selectedReactionsIds:
					t_sbml_id = self.listOfReactions[var].getSbmlId()
					t_name = self.listOfReactions[var].getNameOrSbmlId()
					y_filtered.update({t_name: t_y[t_sbml_id]})

			if self.experiment is not None:
				self.simResults.append((t_t, y_filtered, self.experiment.listOfConditions[i].name))
			else:
				self.simResults.append((t_t, y_filtered, ""))

		# Units and max
		tmax=0
		for time, y_values, _ in self.simResults:
			for key, value in y_values.items():
				for t_value in value:
					tmax = max(tmax, t_value)

		self.y_max = tmax*1.1

		if self.getModelInstance().timeUnits is not None:
			self.t_unit = self.getModelInstance().timeUnits.getName()

		if (self.form.selectedSpeciesIds is not None
			and len(self.form.selectedSpeciesIds) > 0
			and self.listOfVariables[self.form.selectedSpeciesIds[0]].getUnits() is not None):
			self.y_unit = self.listOfVariables[self.form.selectedSpeciesIds[0]].getUnits().getNameOrSbmlId()

		if (self.form.selectedReactionsIds is not None
			and len(self.form.selectedReactionsIds) > 0
			and self.listOfVariables[self.form.selectedReactionsIds[0]].getUnits() is not None):
			self.y_unit = self.listOfVariables[self.form.selectedReactionsIds[0]].getUnits().getNameOrSbmlId()


	def simulateModel(self, request):

		self.form.read(request)
		if not self.form.hasErrors():

			self.experiment = None
			if self.form.experimentId is not None:
				t_experiment = Experiment.objects.get(id=self.experiments[self.form.experimentId].id)
				self.experiment = buildExperiment(t_experiment)

			try:
				t_simulation = TimeseriesSimulation(
					list_of_models=[self.getModelInstance()],
					experiment=self.experiment,
					time_min=self.form.timeMin,
					time_max=self.form.timeMax,
					time_ech=self.form.timeEch)

				t_simulation.run()

				results = t_simulation.getRawData()
				self.read_timeseries(results)

			except LibSigNetSimException as e:
				self.form.addError(e.message)


	def saveSimulation(self, request):

		self.form.read(request)
		if not self.form.hasErrors():

			self.createUniformTimecourse(self.form.timeMin, self.form.timeMax, self.form.timeEch)

			if self.form.experimentId is not None:

				self.loadExperiments(request)
				t_experiment_id = self.experiments[self.form.experimentId].id
				experiment = Experiment.objects.get(id=t_experiment_id)
				conditions = Condition.objects.filter(experiment=experiment)

				for i, condition in enumerate(conditions):
					modifications = []
					input_data = Treatment.objects.filter(condition=condition)
					for data in input_data:

						var = None
						if self.getModelInstance().listOfSpecies.containsName(data.species):
							var = self.getModelInstance().listOfSpecies.getByName(data.species)
						elif self.getModelInstance().listOfParameters.containsName(data.species):
							var = self.getModelInstance().listOfParameters.getByName(data.species)
						elif self.getModelInstance().listOfCompartments.containsName(data.species):
							var = self.getModelInstance().listOfCompartments.getByName(data.species)

						if var is not None:
							modifications.append((var, data.value))

					self.addModel(self.model_filename, modifications)

					variables = []
					if self.form.selectedSpeciesIds is not None:
						for id_var in self.form.selectedSpeciesIds:
							variables.append(self.listOfVariables[id_var])

					if self.form.selectedReactionsIds is not None:
						for id_var in self.form.selectedReactionsIds:
							variables.append(self.listOfVariables[id_var])

					self.addTimeseries(condition.name, variables)
			else:

				self.addModel(self.model_filename)

				variables = []
				if self.form.selectedSpeciesIds is not None:
					for id_var in self.form.selectedSpeciesIds:
						variables.append(self.listOfVariables[id_var])

				if self.form.selectedReactionsIds is not None:
					for id_var in self.form.selectedReactionsIds:
						variables.append(self.listOfVariables[id_var])

				self.addTimeseries("Simulation", variables)

			simulation_filename = join(settings.MEDIA_ROOT, new_sedml_filename())
			open(simulation_filename, "a")
			new_simulation = SEDMLSimulation(project=self.project, name="Simulation", sedml_file=File(open(simulation_filename, "r")))
			new_simulation.save()
			filename = join(settings.MEDIA_ROOT, str(new_simulation.sedml_file))

			self.saveSedml(filename)




	def loadExperiments(self, request):
		self.experiments = Experiment.objects.filter(project=self.project)

	def loadVariables(self):
		self.listOfVariables = [obj for obj in self.getModelInstance().listOfVariables.values() if not obj.constant and (obj.isSpecies() or obj.isParameter() or obj.isCompartment())]

	def loadReactions(self):
		self.listOfReactions = [obj for obj in self.getModelInstance().listOfVariables.values() if obj.isReaction()]

