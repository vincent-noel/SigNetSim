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

class GetCompartment(JsonView, HasWorkingModel):

	def __init__(self):
		JsonView.__init__(self)
		HasWorkingModel.__init__(self)


	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		compartment = self.getModel().listOfCompartments.getBySbmlId(str(request.POST['sbml_id']))
		self.data.update({
			'id': self.getModel().listOfCompartments.values().index(compartment),
			'name': "" if compartment.getName() is None else compartment.getName(),
			'sbml_id': compartment.getSbmlId(),
			'value': compartment.getValue(),
			'constant': (1 if compartment.constant else 0),
			'unit_name': "Choose a unit" if compartment.getUnits() is None else compartment.getUnits().getName(),
			'unit_id': "" if compartment.getUnits() is None else self.getModel().listOfUnitDefinitions.values().index(compartment.getUnits()),
			'notes': "" if compartment.getNotes() is None else compartment.getNotes()
		})
		return JsonView.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)


