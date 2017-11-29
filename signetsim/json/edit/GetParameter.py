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

""" GetParameter.py

	This file...

"""

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class GetParameter(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)


	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)


		parameter = None
		if str(request.POST['reaction']) == "":
			parameter = self.getModel().listOfParameters.getBySbmlId(str(request.POST['sbml_id']))
			self.data.update({
				"reaction_id": "", "reaction_name": "", "id": self.getModel().listOfParameters.values().index(parameter)
			})
		else:
			reaction = self.getModel().listOfReactions[int(request.POST['reaction'])-1]
			parameter = reaction.listOfLocalParameters.getBySbmlId(str(request.POST['sbml_id']))
			self.data.update({
				"reaction_id": (int(request.POST['reaction'])-1), "reaction_name": reaction.getName(),
				"id": reaction.listOfLocalParameters.values().index(parameter)
			})

		self.data.update({
			'name': "" if parameter.getName() is None else parameter.getName(),
			'sbml_id': parameter.getSbmlId(),
			'value': parameter.getValue(),
			'constant': (1 if parameter.constant else 0),
			'unit_name': "Choose a unit" if parameter.getUnits() is None else parameter.getUnits().getName(),
			'unit_id': "" if parameter.getUnits() is None else self.getModel().listOfUnitDefinitions.values().index(parameter.getUnits()),
			'notes': "" if parameter.getNotes() is None else parameter.getNotes()
		})
		if parameter.getAnnotation().getSBOTerm() is not None:
			self.data.update({
				'sboterm': parameter.getAnnotation().getSBOTerm(),
				'sboterm_name': parameter.getAnnotation().getSBOTermDescription()
			})

		return JsonRequest.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)


