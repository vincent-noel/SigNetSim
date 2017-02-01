#!/usr/bin/env python
""" ModelParametersView.py


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
from ModelParametersForm import ModelParametersForm
from libsignetsim.model.ModelException import ModelException

class ModelParametersView(TemplateView, HasWorkingModel, HasErrorMessages):

	template_name = 'edit/parameters.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasErrorMessages.__init__(self)
		HasWorkingModel.__init__(self)

		self.listOfParameters = None
		self.listOfReactions = None
		self.listOfUnits = None

		self.form = ModelParametersForm(self)


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)

		kwargs['list_of_parameters'] = self.listOfParameters
		kwargs['list_of_reactions'] = self.listOfReactions
		kwargs['list_of_units'] = [unit.getNameOrSbmlId() for unit in self.listOfUnits]

		kwargs['form'] = self.form

		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingModel.isChooseModel(self, request):
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "delete":
				self.deleteParameter(request)

			elif request.POST['action'] == "edit":
				self.editParameter(request)

			elif request.POST['action'] == "save":
				self.saveParameter(request)

		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasErrorMessages.clearErrors(self)
		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.loadParameters()
			self.loadReactions()
			self.loadUnits()


	def deleteParameter(self, request):

		parameter_id = self.readInt(request, 'parameter_id',
									"the identifier of the parameter",
									max_value=len(self.listOfParameters),
									reportField=False)

		try:
			t_parameter = self.listOfParameters[parameter_id]
			if parameter_id > len(self.getModel().listOfParameters):
				t_reaction = t_parameter.reaction
				t_reaction.listOfLocalParameters.remove(t_parameter)
			else:
				self.getModel().listOfParameters.remove(t_parameter)

			self.saveModel(request)
			self.loadParameters()

		except ModelException as e:
			self.addError(e.message)


	def editParameter(self, request):

		parameter_id = self.readInt(request, 'parameter_id',
									"the identifier of the parameter",
									max_value=len(self.listOfParameters),
									reportField=False)
		self.form.load(self.listOfParameters[parameter_id])


	def saveParameter(self, request):

		self.form.read(request)
		if not self.form.hasErrors():

			if self.form.isNew():
				parameter = self.getModel().listOfParameters.new()
				self.form.save(parameter)

			else:
				t_param = self.listOfParameters[self.form.id]
				self.form.save(t_param)

			self.saveModel(request)
			self.loadParameters()
			self.form.clear()


	def loadParameters(self):

		self.listOfParameters = self.getModel().listOfParameters.values()
		for reaction in self.getModel().listOfReactions.values():
			self.listOfParameters += reaction.listOfLocalParameters.values()


	def loadReactions(self):
		self.listOfReactions = self.getModel().listOfReactions.values()

	def loadUnits(self):
		self.listOfUnits = self.getModel().listOfUnitDefinitions.values()
