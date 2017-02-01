#!/usr/bin/env python
""" ModelCompartmentsView.py


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
from ModelCompartmentsForm import ModelCompartmentsForm

from libsignetsim.model.ModelException import ModelException


class ModelCompartmentsView(TemplateView, HasWorkingModel, HasErrorMessages):

	template_name = 'edit/compartments.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)
		HasErrorMessages.__init__(self)

		self.listOfCompartments = None
		self.listOfUnits = None
		self.form = ModelCompartmentsForm(self)

	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)
		kwargs['list_of_compartments'] = self.listOfCompartments
		kwargs['list_of_units'] = [unit.getName() for unit in self.listOfUnits]
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

			elif request.POST['action'] == "edit":
				self.edit(request)

			elif request.POST['action'] == "delete":
				self.delete(request)

			elif request.POST['action'] == "save":
				self.save(request)

		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasErrorMessages.clearErrors(self)
		HasWorkingModel.load(self, request, *args, **kwargs)
		if self.isModelLoaded():
			self.listOfCompartments = self.getModel().listOfCompartments.values()
			self.listOfUnits = self.getModel().listOfUnitDefinitions.values()



	def edit(self, request):

		t_id = self.readInt(request, 'compartment_id',
							"the identifier of the compartment",
							max_value=len(self.listOfCompartments))
		self.form.load(t_id)


	def delete(self, request):

		t_id = self.readInt(request, 'compartment_id',
							"the identifier of the compartment",
							max_value=len(self.listOfCompartments))

		try:
			t_compartment = self.listOfCompartments[t_id]
			self.getModel().listOfCompartments.remove(t_compartment)
			self.saveModel(request)
			self.listOfCompartments = self.getModel().listOfCompartments.values()

		except ModelException as e:
			self.addError(e.message)


	def save(self, request):

		self.form.read(request)
		if not self.form.hasErrors():
			if self.form.isNew():
				t_comp = self.getModel().listOfCompartments.new()
				self.form.save(t_comp)

			else:
				t_comp = self.getModel().listOfCompartments[self.listOfCompartments[self.form.id].objId]
				self.form.save(t_comp)

			self.saveModel(request)
			self.listOfCompartments = self.getModel().listOfCompartments.values()
			self.form.clear()
