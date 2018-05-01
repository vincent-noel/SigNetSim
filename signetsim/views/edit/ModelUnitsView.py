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

""" ModelUnitsView.py

	This file ...

"""

from django.views.generic import TemplateView

from signetsim.views.HasWorkingModel import HasWorkingModel
from .ModelUnitsForm import ModelUnitsForm

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

			elif request.POST['action'] == "delete":
				self.deleteUnitDefinition(request)

			elif request.POST['action'] == "save":
				self.saveUnitDefinition(request)

		# self.savePickledModel(request)
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
