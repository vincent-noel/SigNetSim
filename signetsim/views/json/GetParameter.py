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

class GetParameter(JsonView, HasWorkingModel):

	def __init__(self):
		JsonView.__init__(self)
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
			reaction = self.getModel().listOfReactions[int(request.POST['reaction'])]
			parameter = reaction.listOfLocalParameters.getBySbmlId(str(request.POST['sbml_id']))
			self.data.update({
				"reaction_id": int(request.POST['reaction']), "reaction_name": reaction.getName(),
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

		return JsonView.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)


