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

""" SteadyStatesSimulationForm.py

	This file ...

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

		self.timeMax = self.readDuration(request, 'time_max',
							"the end point of the simulation")

		self.steady_states_str = str(request.POST['ss_to_plot'])

		self.steady_states = []
		for t_initval in split(",", self.steady_states_str.strip()):
			self.steady_states.append(float(t_initval))

		self.speciesId = int(request.POST['species_id'])
		self.speciesName = self.parent_view.listOfVariables[self.speciesId].getNameOrSbmlId()