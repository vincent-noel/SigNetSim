#!/usr/bin/env python
""" SteadyStatesSimulationView.py


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

from libsignetsim.simulation.SimulationException import SimulationException
from libsignetsim.data.ExperimentalCondition import ExperimentalCondition
from libsignetsim.data.ExperimentalData import ExperimentalData
from libsignetsim.data.ListOfExperimentalData import ListOfExperimentalData
from libsignetsim.data.Experiment import Experiment as SigNetSimExperiment
from signetsim.models import SbmlModel, Experiment, Condition, Observation, Treatment

from libsignetsim.model.Model import Model
from libsignetsim.model.ModelException import ModelException
from libsignetsim.simulation.SteadyStatesSimulation import SteadyStatesSimulation
from libsignetsim.simulation.SimulationException import SimulationException

from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist

from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.views.simulate.SteadyStatesSimulationForm import SteadyStateSimulationForm
from signetsim.models import SbmlModel
from signetsim.settings.Settings import Settings
# from re import split

class SteadyStateSimulationView(TemplateView, HasWorkingModel):

	template_name = 'simulate/steady_states.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)

		self.form = SteadyStateSimulationForm(self)

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
		# kwargs['experiments'] = self.experiments

		# kwargs['experiment_id'] = self.form.experimentId
		# kwargs['experiment_name'] = self.experimentName
		# kwargs['experiment_nb_conditions'] = self.nbConditions
		# kwargs['experiment_conditions_names'] = self.conditionNames
		# kwargs['experiment_observations'] = self.observations

		kwargs['ids_species_selected'] = self.form.selectedSpeciesIds
		kwargs['ids_reactions_selected'] = self.form.selectedReactionsIds

		kwargs['t_min'] = self.form.timeMin
		# kwargs['t_ech'] = self.form.timeEch
		kwargs['t_max'] = self.form.timeMax

		kwargs['steady_states'] = self.form.steady_states
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

			elif request.POST['action'] == "simulate_steady_states":
				self.simulateModel(request)

		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.loadVariables()
			self.loadReactions()
			self.loadExperiments(request)

	def simulate_steady_states(self, request):


		t_simulation = SteadyStatesSimulation(
							list_of_models=[self.model],
							species_input=self.listOfVariables[self.form.speciesId],
							list_of_initial_values=self.form.steady_states,
							time_min=self.form.timeMin,
							time_max=self.form.timeMax)

		t_simulation.run()

		t_y = {}
		for species in self.form.selectedSpeciesIds:
			t_list = []
			for iss, ss in enumerate(self.form.steady_states):
				t_list.append(t_simulation.listOfData_v2[iss][self.listOfVariables[species].getSbmlId()])

			print t_list
			t_y.update({self.listOfVariables[species].getNameOrSbmlId(): t_list})

		self.simResults = t_y

		#
		#     # species_pos = self.model.listOfSpecies[species[self.speciesId].objId].getPos()
		#     species_pos = t_species.getPos()
		#
		#     self.read_selected_species(request)
		#
		#     request.session['view_width'] = int(request.POST['wdth'])
		#
		#     request.session['species_to_plot'] = self.speciesId
		#     request.session['steady_states_to_plot'] = ss
		#     request.session['steady_states_t_min'] = self.timeMin
		#     request.session['steady_states_t_max'] = self.timeMax
		#     request.session['species_name'] = self.speciesName
		#     request.session['species_pos'] = species_pos
		#
		#     request.session['names_species_selected'] = self.selectedSpeciesNames
		#     request.session['ids_species_selected'] = self.selectedSpeciesIds
		#
		#     t_simulation_data = t_simulation.getSimulationResults()
		#
		#     sim_data = {}
		#     for i_initial_values in range(len(ss)):
		#
		#         y = [[] for _ in self.selectedSpeciesIds]
		#         (t, trajs) = t_simulation_data[i_initial_values]
		#
		#         for i_species, t_species in enumerate(self.selectedSpeciesIds):
		#             y[i_species] = trajs[t_species]
		#
		#         sim_data.update({i_initial_values:(t,y)})
		#
		#     request.session['result_simulation'] = sim_data
		#
		self.simulationResultsLoaded = True

	#
	# def simulate_timeseries(self, request):
	#
	#     self.loadExperiments(request)
	#     self.experiment = None
	#
	#     if self.form.experimentId is not None:
	#         self.buildExperiment(request)
	#
	#
	#     t_simulation = TimeseriesSimulation(
	#         list_of_models=[self.getModelInstance()],
	#         experiment=self.experiment,
	#         time_min=self.form.timeMin,
	#         time_max=self.form.timeMax,
	#         time_ech=self.form.timeEch)
	#
	#     t_simulation.run()
	#
	#     return t_simulation.getRawData()


	def read_timeseries(self, results):

		self.simResults = []
		for result in results:
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

			self.simResults.append((t_t, y_filtered))


		tmax=0
		for time, y_values in self.simResults:
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
			try:
				results = self.simulate_steady_states(request)
				# self.read_timeseries(results)

			except SimulationException as e:
				self.form.addError(e.message)

			except ModelException as e:
				self.form.addError(e.message)


	def loadExperiments(self, request):
		self.experiments = Experiment.objects.filter(project = self.project)

	def loadVariables(self):
		self.listOfVariables = [obj for obj in self.getModelInstance().listOfVariables.values() if not obj.constant and (obj.isSpecies() or obj.isParameter() or obj.isCompartment())]

	def loadReactions(self):
		self.listOfReactions = [obj for obj in self.getModelInstance().listOfVariables.values() if obj.isReaction()]


	#
	#
	#
	# def buildExperiment(self, request):
	#
	#     t_experiment_id = self.experiments[self.form.experimentId].id
	#
	#     experiment = Experiment.objects.get(id=t_experiment_id)
	#
	#     conditions = Condition.objects.filter(experiment=experiment)
	#
	#     self.nbConditions = len(conditions)
	#     self.experimentName = experiment.name
	#     self.experiment = SigNetSimExperiment()
	#     self.conditionNames = []
	#     self.observations = []
	#
	#     for condition in conditions:
	#         self.conditionNames.append(str(condition.name))
	#         observed_data = Observation.objects.filter(condition=condition)
	#         list_of_experimental_data = ListOfExperimentalData()
	#         for data in observed_data:
	#             t_experimental_data = ExperimentalData()
	#             t_experimental_data.readDB(
	#                     data.species, data.time, data.value, data.stddev,
	#                     data.steady_state, data.min_steady_state,
	#                     data.max_steady_state)
	#
	#             list_of_experimental_data.add(t_experimental_data)
	#
	#
	#         if self.form.showObservations == True:
	#             self.observations.append(list_of_experimental_data.getValues())
	#
	#         input_data = Treatment.objects.filter(condition=condition)
	#
	#         list_of_input_data = ListOfExperimentalData()
	#         for data in input_data:
	#             t_experimental_data = ExperimentalData()
	#             t_experimental_data.readDB(
	#                     data.species, data.time, data.value)
	#             list_of_input_data.add(t_experimental_data)
	#
	#         t_condition = ExperimentalCondition()
	#         t_condition.read(list_of_input_data, list_of_experimental_data)
	#         t_condition.name = condition.name
	#
	#         self.experiment.addCondition(t_condition)
	#
	#     self.experiment.name = experiment.name
	#     print self.observations
	#




	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	#
	# def __init__(self, **kwargs):
	#
	#     TemplateView.__init__(self, **kwargs)
	#     HasWorkingModel.__init__(self)
	#
	#     self.listOfSpecies = None
	#
	#     self.selectedSpeciesIds = None
	#     self.selectedSpeciesNames = None
	#
	#     self.speciesId = None
	#     self.speciesName = None
	#
	#     self.timeMin = None
	#     self.timeMax = None
	#
	#     self.simulationResultsLoaded = None
	#     self.errorMessage = None
	#
	#
	# def get_context_data(self, **kwargs):
	#
	#     kwargs = HasWorkingModel.get_context_data(self, **kwargs)
	#
	#     kwargs['species'] = self.listOfSpecies
	#
	#     kwargs['species_id'] = self.speciesId
	#     kwargs['species_name'] = self.speciesName
	#     kwargs['t_min'] = self.timeMin
	#     kwargs['t_max'] = self.timeMax
	#
	#     kwargs['simulation_results_loaded'] = self.simulationResultsLoaded
	#     kwargs['simulation_error_message'] = self.errorMessage
	#
	#     return kwargs
	#
	#
	# def get(self, request, *args, **kwargs):
	#
	#     self.load(request, *args, **kwargs)
	#     return TemplateView.get(self, request, *args, **kwargs)
	#
	#
	# def post(self, request, *args, **kwargs):
	#
	#     self.load(request, *args, **kwargs)
	#
	#     if "action" in request.POST:
	#         if HasWorkingModel.isChooseModel(self, request):
	#             self.load(request, *args, **kwargs)
	#
	#         elif request.POST['action'] == "simulate_steady_states":
	#             self.simulate_steadystates(request)
	#
	#
	#
	#     return TemplateView.get(self, request, *args, **kwargs)
	#
	# def load(self, request, *args, **kwargs):
	#
	#     HasWorkingModel.load(self, request, *args, **kwargs)
	#
	#     if self.isModelLoaded():
	#         self.loadSpecies()
	#
	#
	# def read_selected_species(self, request):
	#
	#     species_selected = request.POST.getlist('species_selected')
	#     species_selected = [int(species) for species in species_selected]
	#
	#     self.selectedSpeciesNames = []
	#     self.selectedSpeciesIds = []
	#     for t_species in self.model.listOfSpecies.values():
	#         if t_species.objId in species_selected:
	#             self.selectedSpeciesNames.append(t_species.name)
	#             self.selectedSpeciesIds.append(t_species.sbmlId)
	#
	#
	# def simulate_steadystates(self, request):
	#
	#     self.model.build()
	#     self.loadSpecies()
	#
	#     self.timeMin = float(request.POST['time_min'])
	#     self.timeMax = float(request.POST['time_max'])
	#     self.speciesId = int(request.POST['species_id'])
	#     t_species = self.listOfSpecies[self.speciesId]
	#     self.speciesName = t_species.name
	#
	#     ss_to_plot = str(request.POST['ss_to_plot'])
	#     ss = split(",", ss_to_plot.strip())
	#
	#     steady_states = []
	#     for t_initval in ss:
	#         steady_states.append([(t_species.sbmlId,
	#                                 float(t_initval))])
	#
	#     t_simulation = SteadyStatesSimulation(
	#                     list_of_models=[self.model],
	#                     list_of_initial_values=steady_states,
	#                     time_min=self.timeMin,
	#                     time_max=self.timeMax)
	#
	#     t_simulation.run()
	#
	#     # species_pos = self.model.listOfSpecies[species[self.speciesId].objId].getPos()
	#     species_pos = t_species.getPos()
	#
	#     self.read_selected_species(request)
	#
	#     request.session['view_width'] = int(request.POST['wdth'])
	#
	#     request.session['species_to_plot'] = self.speciesId
	#     request.session['steady_states_to_plot'] = ss
	#     request.session['steady_states_t_min'] = self.timeMin
	#     request.session['steady_states_t_max'] = self.timeMax
	#     request.session['species_name'] = self.speciesName
	#     request.session['species_pos'] = species_pos
	#
	#     request.session['names_species_selected'] = self.selectedSpeciesNames
	#     request.session['ids_species_selected'] = self.selectedSpeciesIds
	#
	#     t_simulation_data = t_simulation.getSimulationResults()
	#
	#     sim_data = {}
	#     for i_initial_values in range(len(ss)):
	#
	#         y = [[] for _ in self.selectedSpeciesIds]
	#         (t, trajs) = t_simulation_data[i_initial_values]
	#
	#         for i_species, t_species in enumerate(self.selectedSpeciesIds):
	#             y[i_species] = trajs[t_species]
	#
	#         sim_data.update({i_initial_values:(t,y)})
	#
	#     request.session['result_simulation'] = sim_data
	#
	#     self.simulationResultsLoaded = True
	#
	#
	# def loadSpecies(self):
	#     self.listOfSpecies = self.model.listOfSpecies.values()
