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
from libsignetsim.model.sbml.UnitDefinition import Unit, UnitDefinition
class ModelUnitsView(TemplateView, HasWorkingModel):

	template_name = 'edit/units.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)

		self.listOfUnitDefinitions = None

		self.unitDefinition = None
		self.listOfUnits = []

		self.addingNewUnit = None
		self.editingUnitDefinition = None


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)

		kwargs['unit_definitions'] = self.listOfUnitDefinitions



		if self.unitDefinition is not None:
			kwargs['unit_definition_desc'] = self.unitDefinition.printUnitDefinition()
			kwargs['unit_definition_name'] = self.unitDefinition.getName()
			kwargs['unit_definition_identifier'] = self.unitDefinition.getSbmlId()
		else:
			kwargs['unit_definition_desc'] = None
			kwargs['unit_definition_name'] = None
			kwargs['unit_definition_identifier'] = None

		kwargs['units'] = self.listOfUnits

		kwargs['unit_list'] = Unit.unit_id.values()

		kwargs['adding_new_unit'] = self.addingNewUnit
		kwargs['editting_unit'] = self.editingUnitDefinition
		return kwargs


	def get(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingModel.isChooseModel(self, request):
				self.load(request, *args, **kwargs)


			elif request.POST['action'] == "edit_unit_definition":
				self.loadUnitDefinition(request)


			elif request.POST['action'] == "delete_unit_definition":
				t_id = int(request.POST['unit_definition_id'])
				self.getModel().listOfUnitDefinitions.removeById(
										self.listOfUnitDefinitions[t_id].objId)
				self.saveModel(request)
				self.load(request, *args, **kwargs)


			elif request.POST['action'] == "add_unit_definition":
				self.unitDefinition = self.getModel().listOfUnitDefinitions.new()
				self.readForm(request)
				self.saveModel(request)
				self.load(request, *args, **kwargs)


			elif request.POST['action'] == "save_unit_definition":
				self.unitDefinition = self.listOfUnitDefinitions[int(request.POST['unit_definition_id'])]
				self.readForm(request)
				self.saveModel(request)
				self.load(request, *args, **kwargs)


			elif request.POST['action'] == "add_unit":
				self.unitDefinition = self.getModel().listOfUnitDefinitions.new()
				self.readForm(request)
				self.addUnit(request)
				if "unit_definition_id" in request.POST:
					self.editingUnitDefinition = int(request.POST['unit_definition_id'])
				else:
					self.addingNewUnit = True

			elif str(request.POST['action']).startswith("delete_unit_"):
				self.unitDefinition = self.getModel().listOfUnitDefinitions.new()

				self.readForm(request)
				i=0
				while str(request.POST['action']) != ("delete_unit_%d" % i):
					i+= 1

				self.unitDefinition.listOfUnits.pop(i)
				self.listOfUnits.pop(i)
				if "unit_definition_id" in request.POST:
					self.editingUnitDefinition = int(request.POST['unit_definition_id'])
				else:
					self.addingNewUnit = True

		self.load(request, *args, **kwargs)
		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.loadUnitDefinitions()

	def loadUnitDefinition(self, request):

		t_kinds = Unit.unit_id.keys()
		t_id = int(request.POST['unit_definition_id'])
		self.unitDefinition = self.listOfUnitDefinitions[t_id]
		self.listOfUnits = []
		for t_unit in self.unitDefinition.listOfUnits:
			self.listOfUnits.append((t_kinds.index(t_unit.kind),
										t_unit.exponent,
										t_unit.scale,
										t_unit.multiplier,
										t_unit.printUnit()))

		self.editingUnitDefinition = t_id


	def readForm(self, request):

		self.readUnits(request)
		self.unitDefinition.setName(str(request.POST['unit_definition_name']))
		self.unitDefinition.setSbmlId(str(request.POST['unit_definition_identifier']))

	def addUnit(self, request):
		self.listOfUnits.append(self.readUnit(request))

	def readUnits(self, request):

		self.unitDefinition.listOfUnits = []
		i = 0
		while ("unit_id_%d" % i) in request.POST:
			t_kinds = Unit.unit_id.keys()
			t_unit = int(request.POST['unit_id_%d' % i])
			t_exponent = int(request.POST['unit_exponent_%d' % i])
			t_scale = int(request.POST['unit_scale_%d' % i])
			t_multiplier = float(request.POST['unit_multiplier_%d' % i])
			t_object = Unit()
			t_object.new(t_kinds[t_unit], t_exponent, t_scale, t_multiplier)
			self.listOfUnits.append((t_unit,
										t_exponent,
										t_scale,
										t_multiplier,
										t_object.printUnit()))

			self.unitDefinition.listOfUnits.append(t_object)
			i += 1

		self.unitDefinitionDesc = self.unitDefinition.printUnitDefinition()


	def readUnit(self, request):

		t_kinds = Unit.unit_id.keys()

		t_unit = int(request.POST['unit_id'])
		t_exponent = int(request.POST['unit_exponent'])
		t_scale = int(request.POST['unit_scale'])
		t_multiplier = float(request.POST['unit_multiplier'])

		t_object = Unit()
		t_object.new(t_kinds[t_unit], t_exponent, t_scale, t_multiplier)

		self.unitDefinition.listOfUnits.append(t_object)

		return (t_unit, t_exponent, t_scale, t_multiplier, t_object.printUnit())


	def loadUnitDefinitions(self):

		self.listOfUnitDefinitions = self.getModel().listOfUnitDefinitions.values()
