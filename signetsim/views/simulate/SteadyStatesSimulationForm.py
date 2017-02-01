#!/usr/bin/env python
""" SteadyStatesSimulationForm.py


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

from signetsim.views.HasErrorMessages import HasErrorMessages
from re import split


class SteadyStateSimulationForm(HasErrorMessages):


	def __init__(self, parent_view):

		HasErrorMessages.__init__(self)
		self.parent_view = parent_view

		self.selectedSpeciesIds = None
		self.selectedReactionsIds = None

		# self.experimentId = None

		self.timeMin = None
		# self.timeEch = None
		self.timeMax = None
		# self.showObservations = None
		self.steady_states = []
		self.speciesId = None
	# For SED-ML later
	# def load(self):
	#     pass
	#
	# def save(self):
	#     pass


	def read(self, request):

		self.read_selected_species(request)
		self.read_selected_reactions(request)
		self.read_options(request)


	def read_selected_species(self, request):

		self.selectedSpeciesIds = self.readListInt(request, 'species_selected',
									"the list of species to print",
									required=False,
									max_value=len(self.parent_view.listOfVariables))

	def read_selected_reactions(self, request):

		self.selectedReactionsIds = self.readListInt(request, 'reactions_selected',
									"the list of reaction fluxes to print",
									required=False,
									max_value=len(self.parent_view.listOfReactions))


	def read_options(self, request):

		self.timeMin = self.readDuration(request, 'time_min',
							"the starting point of the simulation")
		# self.timeEch = self.readDuration(request, 'time_ech',
		#             "the duration between two time points in the simulation")
		self.timeMax = self.readDuration(request, 'time_max',
							"the end point of the simulation")

		# self.experimentId = self.readInt(request, 'experiment_id',
		#                 "the identifier of the experiment to simulate",
		#                 required=False,
		#                 max_value=len(self.parent_view.experiments))

		# if self.experimentId is not None:
		#     self.showObservations = self.readOnOff(request, 'show_observations',
		#                                 "the checkbox to plot the observations")


		print request.POST.get('ss_to_plot')
		ss_to_plot = str(request.POST['ss_to_plot'])
		ss = split(",", ss_to_plot.strip())

		self.steady_states = []
		for t_initval in ss:
			self.steady_states.append(float(t_initval))

		self.speciesId = int(request.POST['species_id'])
		# t_species = self.parent_view.listOfSpecies[self.speciesId]
	#
	#
	#
	# template_name = 'simulate/steady_states.html'
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
