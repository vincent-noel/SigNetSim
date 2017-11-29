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

""" TimeSeriesSimulationForm.py

	This file ...

"""

from signetsim.views.HasErrorMessages import HasErrorMessages

class TimeSeriesSimulationForm(HasErrorMessages):


	def __init__(self, parent_view):

		HasErrorMessages.__init__(self)
		self.parent_view = parent_view

		self.simulationName = None
		self.simulationModelSnapshot = None

		self.selectedSpeciesIds = None
		self.selectedReactionsIds = None

		self.experimentId = None

		self.timeMin = None
		self.timeEch = None
		self.timeMax = None
		self.showObservations = None


	def read(self, request):

		self.read_selected_species(request)
		self.read_selected_reactions(request)
		if (len(self.selectedReactionsIds) + len(self.selectedSpeciesIds)) == 0 and self.nbErrors == 0:
			self.addError("Please choose something to plot")
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

		self.simulationName = self.readString(request, "simulation_name",
											  "The name of the simulation", required=False)
		self.saveModelSnapshot = self.readOnOff(request, "simulation_model_snapshot",
											 "The snapshot setting of the simulation")

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
