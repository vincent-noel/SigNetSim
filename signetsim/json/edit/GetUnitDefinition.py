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

""" GetUnitDefinition.py

	This file...

"""

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel
from libsignetsim.model.sbml.Unit import Unit

class GetUnitDefinition(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)

	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		unit_definition_id = int(request.POST['id'])
		unit_definition = self.getModel().listOfUnitDefinitions.values()[unit_definition_id]

		self.data.update({
			'unit_id': unit_definition.getSbmlId(),
			'name': unit_definition.getName(),
			'desc': unit_definition.printUnitDefinition(),
			'list_of_units': [
				(
					str(unit), Unit.unit_id.keys().index(unit.getKind()), unit.getKindName(),
					unit.getExponent(), unit.getScale(), unit.getMultiplier()
				)
				for unit in unit_definition.listOfUnits
			]
		})

		return JsonRequest.post(self, request, *args, **kwargs)
