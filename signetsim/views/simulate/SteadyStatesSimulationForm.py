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

		# self.timeMin = None
		self.timeMax = None
		self.steady_states_str = None
		self.steady_states = []
		self.speciesId = None
		self.speciesName = None

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

		# self.timeMin = self.readDuration(request, 'time_min',
		# 					"the starting point of the simulation")
		self.timeMax = self.readDuration(request, 'time_max',
							"the end point of the simulation")

		self.steady_states_str = str(request.POST['ss_to_plot'])

		self.steady_states = []
		for t_initval in split(",", self.steady_states_str.strip()):
			self.steady_states.append(float(t_initval))

		self.speciesId = int(request.POST['species_id'])
		self.speciesName = self.parent_view.listOfVariables[self.speciesId].getNameOrSbmlId()