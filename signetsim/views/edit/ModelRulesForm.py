#!/usr/bin/env python
""" ModelRulesForm.py


	This file ...


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


	def clear(self):

		ModelParentForm.clear(self)
		self.ruleType = None
		self.variable = None
		self.definition = None


	def load(self, rule_id):

		self.id = rule_id
		t_rule = self.parent.listOfRules[rule_id]

		if self.id < len(self.parent.getModel().listOfRules):
			if t_rule.isAlgebraic():
				self.ruleType = 0
			elif t_rule.isAssignment():
				self.ruleType = 1
			elif t_rule.isRate():
				self.ruleType = 2
		else:
			self.ruleType = 3

		if self.ruleType != 0:
			print "loading rule. variable = %s" % t_rule.getVariable().getNameOrSbmlId()
			self.variable = self.parent.listOfVariables.index(t_rule.getVariable())

		self.definition = t_rule.getExpression()

		self.isEditing = True

	def save(self, rule):

		try:
			if not rule.isAlgebraic():
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
		#
		# print self.ruleType
		# print self.parent.ruleTypes
		print request.POST
		if self.ruleType is not None:

			if self.ruleType in [1,2,3]:

				print "var id = %d" % int(request.POST['variable_id'])
				self.variable = self.readInt(request, 'variable_id',
									"the variable affected",
									max_value=len(self.parent.listOfVariables))
				print [var.getSbmlId() for var in self.parent.listOfVariables]
				print ">> %d" % self.variable

				self.definition = self.readMath(request, 'rule_expression',
										"the mathematical formula")

			else:
				self.definition = self.readMath(request, 'rule_expression_alg',
										"the mathematical formula")


		self.printErrors()
