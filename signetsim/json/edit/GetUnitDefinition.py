#!/usr/bin/env python
""" GetUnitDefinition.py


	This file...

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

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


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
					str(unit), unit.getKind(), unit.getKindName(),
					unit.getExponent(), unit.getScale(), unit.getMultiplier()
				)
				for unit in unit_definition.listOfUnits
			]
		})

		return JsonRequest.post(self, request, *args, **kwargs)
