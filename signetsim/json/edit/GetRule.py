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
from libsignetsim.model.Model import Model
from libsignetsim.model.ModelException import ModelException
from libsignetsim.model.SbmlDocument import SbmlDocument
from os.path import join

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class GetRule(JsonRequest, HasWorkingModel):


	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)

		self.listOfVariables = []

	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		rule_ind = int(request.POST['rule_ind'])
		self.data.update({'rule_id': rule_ind})

		if rule_ind < len(self.getModel().listOfRules):
			rule = self.getModel().listOfRules.values()[rule_ind]
			self.data.update({'rule_type': rule.getRuleType(), 'rule_type_label': rule.getRuleTypeDescription()})


		else:
			rule_ind -= len(self.getModel().listOfRules)
			rule = self.getModel().listOfInitialAssignments.values()[rule_ind]
			self.data.update({'rule_type': 3, 'rule_type_label': 'Initial assignment'})

		self.data.update({
			'expression': rule.getPrettyPrintDefinition()
		})

		if self.data['rule_type'] != 0:
			self.data.update({
				'variable': self.listOfVariables.index(rule.getVariable()),
				'variable_label': rule.getVariable().getNameOrSbmlId()
			})


		return JsonRequest.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)



		for variable in self.getModel().listOfVariables.values():
			if (variable.isParameter()
				or variable.isSpecies()
				or variable.isCompartment()) and variable.isGlobal():

				self.listOfVariables.append(variable)