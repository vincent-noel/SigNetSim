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

from signetsim.models import SbmlModel, Experiment, Condition, Observation, Treatment

from libsignetsim.LibSigNetSimException import LibSigNetSimException
from libsignetsim.simulation.SteadyStatesSimulation import SteadyStatesSimulation

from django.views.generic import TemplateView

from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.views.simulate.SteadyStatesSimulationForm import SteadyStateSimulationForm
from signetsim.settings.Settings import Settings

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


	# def read_timeseries(self, results):
	#
	# 	self.simResults = []
	# 	for result in results:
	# 		(t_t, t_y) = result
	#
	# 		y_filtered = {}
	# 		if self.form.selectedSpeciesIds is not None:
	# 			for var in self.form.selectedSpeciesIds:
	# 				t_sbml_id = self.listOfVariables[var].getSbmlId()
	# 				t_name = self.listOfVariables[var].getNameOrSbmlId()
	# 				if self.form.showObservations == True:
	# 					t_name += " (model)"
	# 				y_filtered.update({t_name:t_y[t_sbml_id]})
	#
	# 		if self.form.selectedReactionsIds is not None:
	# 			for var in self.form.selectedReactionsIds:
	# 				t_sbml_id = self.listOfReactions[var].getSbmlId()
	# 				t_name = self.listOfReactions[var].getNameOrSbmlId()
	# 				y_filtered.update({t_name:t_y[t_sbml_id]})
	#
	# 		self.simResults.append((t_t, y_filtered))
	#
	#
	# 	tmax=0
	# 	for time, y_values in self.simResults:
	# 		for key, value in y_values.items():
	# 			for t_value in value:
	# 				tmax = max(tmax, t_value)
	#
	# 	self.y_max = tmax*1.1
	#
		# if self.getModelInstance().timeUnits is not None:
		# 	self.t_unit = self.getModelInstance().timeUnits.getName()
		#
		# if (self.form.selectedSpeciesIds is not None
		# 	and len(self.form.selectedSpeciesIds) > 0
		# 	and self.listOfVariables[self.form.selectedSpeciesIds[0]].getUnits() is not None):
		# 	self.y_unit = self.listOfVariables[self.form.selectedSpeciesIds[0]].getUnits().getNameOrSbmlId()
		#
		# if (self.form.selectedReactionsIds is not None
		# 	and len(self.form.selectedReactionsIds) > 0
		# 	and self.listOfVariables[self.form.selectedReactionsIds[0]].getUnits() is not None):
		# 	self.y_unit = self.listOfVariables[self.form.selectedReactionsIds[0]].getUnits().getNameOrSbmlId()

	def simulateModel(self, request):

		self.form.read(request)
		if not self.form.hasErrors():
			try:
				self.simulate_steady_states(request)

			except LibSigNetSimException as e:
				self.form.addError(e.message)

	def loadExperiments(self, request):
		self.experiments = Experiment.objects.filter(project = self.project)

	def loadVariables(self):
		self.listOfVariables = [obj for obj in self.getModelInstance().listOfVariables.values() if not obj.constant and (obj.isSpecies() or obj.isParameter() or obj.isCompartment())]

	def loadReactions(self):
		self.listOfReactions = [obj for obj in self.getModelInstance().listOfVariables.values() if obj.isReaction()]

