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

""" SteadyStatesSimulationView.py

	This file ...

"""

from django.views.generic import TemplateView

from libsignetsim.LibSigNetSimException import LibSigNetSimException
from libsignetsim.simulation.SteadyStatesSimulation import SteadyStatesSimulation

from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.views.simulate.SedmlWriter import SedmlWriter
from signetsim.views.simulate.SteadyStatesSimulationForm import SteadyStateSimulationForm
from signetsim.models import Experiment, SEDMLSimulation, new_sedml_filename
from signetsim.settings.Settings import Settings

from django.conf import settings
from django.core.files import File

from os.path import join

class SteadyStateSimulationView(TemplateView, HasWorkingModel, SedmlWriter):

	template_name = 'simulate/steady_states.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)
		SedmlWriter.__init__(self)

		self.form = SteadyStateSimulationForm(self)

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
		self.conditionNames = None

	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)

		kwargs['species'] = self.listOfVariables
		kwargs['reactions'] = self.listOfReactions

		kwargs['ids_species_selected'] = self.form.selectedSpeciesIds
		kwargs['ids_reactions_selected'] = self.form.selectedReactionsIds

		kwargs['steady_states'] = self.form.steady_states
		kwargs['sim_results'] = self.simResults
		kwargs['t_unit'] = self.t_unit
		kwargs['y_unit'] = self.y_unit
		kwargs['y_max'] = self.y_max
		kwargs['colors'] = Settings.default_colors

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

			elif request.POST['action'] == "simulate_steady_states":
				self.simulateModel(request)

			elif request.POST['action'] == "save_simulation":
				self.saveSimulation(request)

		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.loadVariables()
			self.loadReactions()
			self.loadExperiments()

	def simulate_steady_states(self, request):

		t_simulation = SteadyStatesSimulation(
							list_of_models=[self.model],
							species_input=self.listOfVariables[self.form.speciesId],
							list_of_initial_values=self.form.steady_states,
		)

		t_simulation.run()
		t_y = {}
		for species in self.form.selectedSpeciesIds:
			t_list = t_simulation.getRawData()[self.listOfVariables[species].getSbmlId()]
			t_y.update({self.listOfVariables[species].getNameOrSbmlId(): t_list})
		for reaction in self.form.selectedReactionsIds:
			t_list = t_simulation.getRawData()[self.listOfReactions[reaction].getSbmlId()]
			t_y.update({self.listOfReactions[reaction].getNameOrSbmlId(): t_list})
		self.simResults = t_y

	def simulateModel(self, request):

		self.form.read(request)
		if not self.form.hasErrors():
			try:
				self.simulate_steady_states(request)

			except LibSigNetSimException as e:
				self.form.addError(e.message)

	def saveSimulation(self, request):

		self.form.read(request)
		if not self.form.hasErrors():
			self.createDocument()
			steady_states = self.createSteadyStates()

			variables = []
			if self.form.selectedSpeciesIds is not None:
				for id_var in self.form.selectedSpeciesIds:
					variables.append(self.listOfVariables[id_var])

			if self.form.selectedReactionsIds is not None:
				for id_var in self.form.selectedReactionsIds:
					variables.append(self.listOfVariables[id_var])

			model = self.addModel(self.model_filename, var_input=self.listOfVariables[self.form.speciesId])
			self.addSteadyStatesCurve(steady_states, model, "Simulation", variables, self.form.steady_states, self.listOfVariables[self.form.speciesId])

			simulation_filename = join(settings.MEDIA_ROOT, new_sedml_filename())
			open(simulation_filename, "a")
			new_simulation = SEDMLSimulation(project=self.project, name="Simulation", sedml_file=File(open(simulation_filename, "r")))
			new_simulation.save()
			filename = join(settings.MEDIA_ROOT, str(new_simulation.sedml_file))

			self.saveSedml(filename)

	def loadExperiments(self):
		self.experiments = Experiment.objects.filter(project = self.project)

	def loadVariables(self):
		self.listOfVariables = [obj for obj in self.getModelInstance().listOfVariables.values() if not obj.constant and (obj.isSpecies() or obj.isParameter() or obj.isCompartment())]

	def loadReactions(self):
		self.listOfReactions = [obj for obj in self.getModelInstance().listOfVariables.values() if obj.isReaction()]

