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

""" ModelRulesForm.py

	This file ...

"""

from django.views.generic import TemplateView
from signetsim.views.HasWorkingModel import HasWorkingModel
from libsignetsim.model.ModelException import ModelException
from ModelParentForm import ModelParentForm

class ModelRulesForm(ModelParentForm):

	def __init__(self, parent):

		ModelParentForm.__init__(self, parent)

		self.ruleType = None
		self.variable = None
		self.definition = None


	def save(self, rule):

		try:
			if self.ruleType > 0:
				rule.setVariable(self.parent.listOfVariables[self.variable])

			rule.setPrettyPrintDefinition(self.definition)

		except ModelException as e:
			self.addError(e.message)


	def read(self, request):

		self.id = self.readInt(request, 'rule_id',
								"the indice of the rule",
								max_value=len(self.parent.listOfRules),
								required=False)

		self.ruleType = self.readInt(request, 'rule_type',
								"the type of rule",
								max_value=len(self.parent.ruleTypes))

		if self.ruleType is not None:
			if self.ruleType > 0:
				self.variable = self.readInt(request, 'variable_id',
									"the variable affected",
									max_value=len(self.parent.listOfVariables))

				self.definition = self.readMath(request, 'rule_expression',
										"the mathematical formula")

			else:
				self.definition = self.readMath(request, 'rule_expression_alg',
										"the mathematical formula")
