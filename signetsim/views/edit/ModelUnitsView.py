#!/usr/bin/env python
""" ModelUnitsView.py


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
from signetsim.views.edit.ModelUnitsForm import ModelUnitsForm

from libsignetsim.model.sbml.Unit import Unit


class ModelUnitsView(TemplateView, HasWorkingModel):

	template_name = 'edit/units.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)

		self.listOfUnitDefinitions = None
		self.form = ModelUnitsForm(self)

	def get_context_data(self, **kwargs):
		kwargs = HasWorkingModel.get_context_data(self, **kwargs)

		kwargs['unit_definitions'] = self.listOfUnitDefinitions
		kwargs['unit_list'] = Unit.unit_id.values()

		return kwargs

	def get(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingModel.isChooseModel(self, request):
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "delete":
				self.deleteUnitDefinition(request)

			elif request.POST['action'] == "save":
				print "> Saving..."
				self.saveUnitDefinition(request)

		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)

	def deleteUnitDefinition(self, request):
		t_id = int(request.POST['id'])
		t_unit_definition = self.getModel().listOfUnitDefinitions.values()[t_id]
		self.getModel().listOfUnitDefinitions.remove(t_unit_definition)
		self.loadUnitDefinitions()
		self.saveModel(request)

	def saveUnitDefinition(self, request):

		self.form.read(request)
		if not self.form.hasErrors():
			if self.form.isNew():
				unit_definition = self.getModel().listOfUnitDefinitions.new()
				self.form.save(unit_definition)
			else:
				print ">> existing"
				unit_definition = self.getModel().listOfUnitDefinitions.values()[self.form.id]
				self.form.save(unit_definition)

		self.loadUnitDefinitions()
		self.saveModel(request)

	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.loadUnitDefinitions()

	def loadUnitDefinitions(self):

		self.listOfUnitDefinitions = [unit.getNameOrSbmlId() for unit in self.getModel().listOfUnitDefinitions.values()]
