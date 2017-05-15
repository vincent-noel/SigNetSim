#!/usr/bin/env python
""" TimeSeriesSimulationView.py


	This file ...


	Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published
	by the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

from libsignetsim.model.Model import Model
from libsignetsim.model.ModelException import ModelException
from libsignetsim.simulation.TimeseriesSimulation import TimeseriesSimulation
from libsignetsim.simulation.SimulationException import SimulationException
from libsignetsim.data.ExperimentalCondition import ExperimentalCondition
from libsignetsim.data.ExperimentalData import ExperimentalData
from libsignetsim.data.ListOfExperimentalData import ListOfExperimentalData
from libsignetsim.data.Experiment import Experiment as SigNetSimExperiment

from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.conf import settings
from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.models import SbmlModel, Experiment, Condition, Observation, Treatment, SEDMLSimulation
from signetsim.settings.Settings import Settings
from TimeSeriesSimulationForm import TimeSeriesSimulationForm

from libsignetsim.sedml.SedmlDocument import SedmlDocument
from os.path import basename, join
from django.core.files import File


class TimeSeriesSimulationView(TemplateView, HasWorkingModel):

	template_name = 'simulate/timeseries.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)

		self.form = TimeSeriesSimulationForm(self)

		self.listOfVariables = None
		self.listOfReactions = None
		self.experiments = None
		self.nbConditions = None
		self.experimentName = None

		self.observations = None

		self.simulationResultsLoaded = None
		self.ts = None
		self.ys = None
		self.simResults = None
		self.t_unit = None
		self.y_unit = None
		self.y_max = 0
		self.conditionNames = None

	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)

		kwargs['species'] = self.listOfVariables
		kwargs['reactions'] = self.listOfReactions
		kwargs['experiments'] = self.experiments

		kwargs['experiment_id'] = self.form.experimentId
		kwargs['experiment_name'] = self.experimentName
		kwargs['experiment_nb_conditions'] = self.nbConditions
		kwargs['experiment_conditions_names'] = self.conditionNames
		kwargs['experiment_observations'] = self.observations

		kwargs['ids_species_selected'] = self.form.selectedSpeciesIds
		kwargs['ids_reactions_selected'] = self.form.selectedReactionsIds

		kwargs['t_min'] = self.form.timeMin
		kwargs['t_ech'] = self.form.timeEch
		kwargs['t_max'] = self.form.timeMax

		kwargs['sim_results'] = self.simResults
		kwargs['t_unit'] = self.t_unit
		kwargs['y_unit'] = self.y_unit
		kwargs['y_max'] = self.y_max
		kwargs['colors'] = Settings.default_colors

		kwargs['simulation_results_loaded'] = self.simulationResultsLoaded

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

		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.loadVariables()
			self.loadReactions()
			self.loadExperiments(request)




	def simulate_timeseries(self, request):

		self.loadExperiments(request)
		self.experiment = None

		if self.form.experimentId is not None:
			self.buildExperiment(request)


		t_simulation = TimeseriesSimulation(
			list_of_models=[self.getModelInstance()],
			experiment=self.experiment,
			time_min=self.form.timeMin,
			time_max=self.form.timeMax,
			time_ech=self.form.timeEch)

		t_simulation.run()

		return t_simulation.getRawData()


	def read_timeseries(self, results):

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
					y_filtered.update({t_name:t_y[t_sbml_id]})

			if self.form.selectedReactionsIds is not None:
				for var in self.form.selectedReactionsIds:
					t_sbml_id = self.listOfReactions[var].getSbmlId()
					t_name = self.listOfReactions[var].getNameOrSbmlId()
					y_filtered.update({t_name:t_y[t_sbml_id]})

			self.simResults.append((t_t, y_filtered, self.experiment.listOfConditions[i].name))


		tmax=0
		for time, y_values,_ in self.simResults:
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

		self.simulationResultsLoaded = True


	def simulateModel(self, request):

		self.form.read(request)
		if not self.form.hasErrors():

			self.loadExperiments(request)
			self.experiment = None

			if self.form.experimentId is not None:
				self.buildExperiment(request)

			t_simulation = TimeseriesSimulation(
				list_of_models=[self.getModelInstance()],
				experiment=self.experiment,
				time_min=self.form.timeMin,
				time_max=self.form.timeMax,
				time_ech=self.form.timeEch)

			t_simulation.run()
			try:
				results = self.simulate_timeseries(request)
				self.read_timeseries(results)

			except SimulationException as e:
				self.form.addError(e.message)

			except ModelException as e:
				self.form.addError(e.message)





	def saveSimulation(self, request):

		self.form.read(request)
		if not self.form.hasErrors():


			sedml_doc = SedmlDocument()

			simulation = sedml_doc.listOfSimulations.createUniformTimeCourse()
			simulation.setInitialTime(self.form.timeMin)
			simulation.setOutputStartTime(self.form.timeMin)
			simulation.setOutputEndTime(self.form.timeMax)
			simulation.setNumberOfPoints(int((self.form.timeMax-self.form.timeMin)/self.form.timeEch))
			simulation.getAlgorithm().setCVODE()



			self.loadExperiments(request)
			t_experiment_id = self.experiments[self.form.experimentId].id
			experiment = Experiment.objects.get(id=t_experiment_id)
			conditions = Condition.objects.filter(experiment=experiment)

			self.nbConditions = len(conditions)
			self.experimentName = experiment.name
			self.experiment = SigNetSimExperiment()
			self.conditionNames = []
			self.observations = []

			for i, condition in enumerate(conditions):
				input_data = Treatment.objects.filter(condition=condition)

				model = sedml_doc.listOfModels.createModel()
				model.setLanguageSbml()
				model.setSource(self.model_filename)

				for data in input_data:

					var = None
					if self.getModel().listOfSpecies.containsName(data.species):
						var = self.getModel().listOfSpecies.getByName(data.species)
					elif self.getModel().listOfParameters.containsName(data.species):
						var = self.getModel().listOfParameters.getByName(data.species)
					elif self.getModel().listOfCompartments.containsName(data.species):
						var = self.getModel().listOfCompartments.getByName(data.species)

					if var is not None:
						change = model.listOfChanges.createChangeAttribute()
						change.setTarget(var)
						change.setNewValue(data.value)

				task = sedml_doc.listOfTasks.createTask()
				task.setModel(model)
				task.setSimulation(simulation)

				data_time = sedml_doc.listOfDataGenerators.createDataGenerator()
				data_time.setName("Time")
				var_time = data_time.listOfVariables.createVariable("time_%d" % i)
				var_time.setTask(task)
				var_time.setModel(model)
				var_time.setSymbolTime()
				data_time.getMath().setInternalMathFormula(var_time.getSympySymbol())

				plot2D = sedml_doc.listOfOutputs.createPlot2D()

				plot2D.setName(str(condition.name))
				i_var = 0
				if self.form.selectedSpeciesIds is not None:
					for i_var in self.form.selectedSpeciesIds:
						i_var += 1
						data = sedml_doc.listOfDataGenerators.createDataGenerator("data_%d_%d" % (i, i_var))
						data.setName(self.listOfVariables[i_var].getNameOrSbmlId())
						var = data.listOfVariables.createVariable("var_%d_%d" % (i, i_var))
						var.setTask(task)
						var.setModel(model)
						var.setTarget(self.listOfVariables[i_var])
						data.getMath().setInternalMathFormula(var.getSympySymbol())

						curve = plot2D.listOfCurves.createCurve("curve_%d_%d" % (i, i_var))
						curve.setXData(data_time)
						curve.setYData(data)


				if self.form.selectedReactionsIds is not None:
					for i_var in self.form.selectedReactionsIds:
						i_var += 1
						data = sedml_doc.listOfDataGenerators.createDataGenerator("data_%d_%d" % (i, i_var))
						data.setName(self.listOfVariables[i_var].getNameOrSbmlId())
						var = data.listOfVariables.createVariable("var_%d_%d" % (i, i_var))
						var.setTask(task)
						var.setModel(model)
						var.setTarget(self.listOfVariables[i_var])
						data.getMath().setInternalMathFormula(var.getSympySymbol())

						curve = plot2D.listOfCurves.createCurve("curve_%d_%d" % (i, i_var))
						curve.setXData(data_time)
						curve.setYData(data)



			open("simulation.xml", "a")

			new_simulation = SEDMLSimulation(project=self.project, name="Simulation", sedml_file=File(open("simulation.xml", "r")))
			new_simulation.save()

			filename = join(settings.MEDIA_ROOT, str(new_simulation.sedml_file))
			sedml_doc.writeSedmlToFile(filename)





	def loadExperiments(self, request):
		self.experiments = Experiment.objects.filter(project = self.project)

	def loadVariables(self):
		self.listOfVariables = [obj for obj in self.getModelInstance().listOfVariables.values() if not obj.constant and (obj.isSpecies() or obj.isParameter() or obj.isCompartment())]

	def loadReactions(self):
		self.listOfReactions = [obj for obj in self.getModelInstance().listOfVariables.values() if obj.isReaction()]


	def buildExperiment(self, request):

		t_experiment_id = self.experiments[self.form.experimentId].id

		experiment = Experiment.objects.get(id=t_experiment_id)

		conditions = Condition.objects.filter(experiment=experiment)

		self.nbConditions = len(conditions)
		self.experimentName = experiment.name
		self.experiment = SigNetSimExperiment()
		self.conditionNames = []
		self.observations = []

		for condition in conditions:
			self.conditionNames.append(str(condition.name))
			observed_data = Observation.objects.filter(condition=condition)
			list_of_experimental_data = ListOfExperimentalData()
			for data in observed_data:
				t_experimental_data = ExperimentalData()
				t_experimental_data.readDB(
						data.species, data.time, data.value, data.stddev,
						data.steady_state, data.min_steady_state,
						data.max_steady_state)

				list_of_experimental_data.add(t_experimental_data)


			if self.form.showObservations == True:
				self.observations.append(list_of_experimental_data.getValues())

			input_data = Treatment.objects.filter(condition=condition)

			list_of_input_data = ListOfExperimentalData()
			for data in input_data:
				t_experimental_data = ExperimentalData()
				t_experimental_data.readDB(
						data.species, data.time, data.value)
				list_of_input_data.add(t_experimental_data)

			t_condition = ExperimentalCondition()
			t_condition.read(list_of_input_data, list_of_experimental_data)
			t_condition.name = condition.name

			self.experiment.addCondition(t_condition)

		self.experiment.name = experiment.name
