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

""" GetRule.py

	This file...

"""

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
			rule = self.getModel().listOfRules[rule_ind]
			self.data.update({'rule_type': rule.getRuleType(), 'rule_type_label': rule.getRuleTypeDescription()})


		else:
			rule_ind -= len(self.getModel().listOfRules)
			rule = self.getModel().listOfInitialAssignments[rule_ind]
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

		for variable in self.getModel().listOfVariables:
			if ((variable.isParameter() and variable.isGlobal())
				or variable.isSpecies()
				or variable.isCompartment()
				or variable.isStoichiometry()):

				self.listOfVariables.append(variable)