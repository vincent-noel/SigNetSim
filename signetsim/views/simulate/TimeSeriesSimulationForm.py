#!/usr/bin/env python
""" TimeSeriesSimulationForm.py


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

class TimeSeriesSimulationForm(HasErrorMessages):


	def __init__(self, parent_view):

		HasErrorMessages.__init__(self)
		self.parent_view = parent_view

		self.selectedSpeciesIds = None
		self.selectedReactionsIds = None

		self.experimentId = None

		self.timeMin = None
		self.timeEch = None
		self.timeMax = None
		self.showObservations = None

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
		self.timeEch = self.readDuration(request, 'time_ech',
					"the duration between two time points in the simulation")
		self.timeMax = self.readDuration(request, 'time_max',
							"the end point of the simulation")

		self.experimentId = self.readInt(request, 'experiment_id',
						"the identifier of the experiment to simulate",
						required=False,
						max_value=len(self.parent_view.experiments))

		if self.experimentId is not None:
			self.showObservations = self.readOnOff(request, 'show_observations',
										"the checkbox to plot the observations")
