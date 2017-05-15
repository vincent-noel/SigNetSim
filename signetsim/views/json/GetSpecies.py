#!/usr/bin/env python
""" GetSpecies.py


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

from django.conf import settings
from os.path import join

from signetsim.views.json.JsonView import JsonView
from signetsim.views.HasWorkingModel import HasWorkingModel
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.model.Model import Model
from libsignetsim.model.ModelException import ModelException

class GetSpecies(JsonView, HasWorkingModel):

	def __init__(self):
		JsonView.__init__(self)
		HasWorkingModel.__init__(self)


	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		species = self.getModel().listOfSpecies.getBySbmlId(str(request.POST['sbml_id']))

		self.data.update({
			'id': self.getModel().listOfSpecies.values().index(species),
			'name': "" if species.getName() is None else species.getName(),
			'sbml_id': species.getSbmlId(),
			'compartment_name': species.getCompartment().getNameOrSbmlId(),
			'compartment_id': self.getModel().listOfCompartments.values().index(species.getCompartment()),
			'value': species.getValue(),
			'isConcentration': 1 if not species.hasOnlySubstanceUnits else 0,
			'constant': (1 if species.constant else 0),
			'boundaryCondition': (1 if species.boundaryCondition else 0),
			'notes': "" if species.getNotes() is None else species.getNotes(),
		})

		if species.getUnits() is not None:
			self.data.update({
				'unit_name': "" if species.getUnits().getName() is None else species.getUnits().getName(),
				'unit_id': self.getModel().listOfUnitDefinitions.values().index(species.getUnits()),
			})

		return JsonView.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)


