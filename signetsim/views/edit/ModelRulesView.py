#!/usr/bin/env python
""" ModelRulesView.py


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
from signetsim.views.HasErrorMessages import HasErrorMessages
from libsignetsim.model.ModelException import ModelException
from ModelRulesForm import ModelRulesForm
class ModelRulesView(TemplateView, HasWorkingModel, HasErrorMessages):

	template_name = 'edit/rules.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasErrorMessages.__init__(self)
		HasWorkingModel.__init__(self)

		self.listOfVariables = None
		self.listOfRules = None

		self.ruleTypes = ["Algebraic rule",
							"Assignment rule",
							"Rate rule",
							"Initial assignment"]

		self.form = ModelRulesForm(self)

	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)

		kwargs['list_of_variables'] = [var.getNameOrSbmlId() for var in self.listOfVariables]
		kwargs['list_of_rules'] = self.listOfRules
		kwargs['rules_types'] = self.ruleTypes
		kwargs['form'] = self.form

		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		if "action" in request.POST:
			if HasWorkingModel.isChooseModel(self, request):
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == 'delete':
				self.delete(request)

			# elif request.POST['action'] == "edit":
			# 	self.edit(request)

			elif request.POST['action'] == "save":
				self.save(request)

		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasErrorMessages.clearErrors(self)
		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.loadRules()
			self.loadGlobalVariables()


	def save(self, request):

		self.form.read(request)
		if not self.form.hasErrors():
			if self.form.isNew():
				if self.form.ruleType == 0:
					self.getModel().listOfRules.newAlgebraicRule(self.form.definition)

				elif self.form.ruleType == 1:
					self.getModel().listOfRules.newAssignmentRule(self.listOfVariables[self.form.variable],
																self.form.definition)

				elif self.form.ruleType == 2:
					self.getModel().listOfRules.newRateRule(self.listOfVariables[self.form.variable],
																self.form.definition)

				elif self.form.ruleType == 3:
					self.getModel().listOfInitialAssignments.new(self.listOfVariables[self.form.variable],
																self.form.definition)

			else:
				t_rule = self.listOfRules[self.form.id]
				self.form.save(t_rule)

			self.saveModel(request)
			self.loadRules()

		else:
			self.form.printErrors()
			self.printErrors()


	def delete(self, request):

		t_id = self.readInt(request, 'rule_id',
							"the identifier of the rule",
							max_value=len(self.listOfRules))

		t_rule = self.listOfRules[t_id]

		try:
			if t_id < len(self.getModel().listOfRules):
				self.getModel().listOfRules.remove(t_rule)
			else:
				self.getModel().listOfInitialAssignments.remove(t_rule)

		except ModelException as e:
			self.form.addError(e.message)

		self.saveModel(request)
		self.loadRules()


	def loadGlobalVariables(self):

		self.listOfVariables = []
		for variable in self.getModel().listOfVariables.values():
			if ((variable.isParameter() and variable.isGlobal())
				or variable.isSpecies()
				or variable.isCompartment()
				or variable.isStoichiometry()):
				self.listOfVariables.append(variable)


	def loadRules(self):
		self.listOfRules = (self.getModel().listOfRules.values()
			+ self.getModel().listOfInitialAssignments.values())
