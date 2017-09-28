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

""" ModelEventsView.py

	This file ...

"""

from django.views.generic import TemplateView
from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.views.HasErrorMessages import HasErrorMessages
from ModelEventsForm import ModelEventsForm

from libsignetsim.model.ModelException import ModelException


class ModelEventsView(TemplateView, HasWorkingModel, HasErrorMessages):

	template_name = 'edit/events.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasErrorMessages.__init__(self)
		HasWorkingModel.__init__(self)

		self.listOfVariables = None
		self.listOfEvents = None
		self.form = ModelEventsForm(self)

	def get_context_data(self, **kwargs):

		kwargs = HasErrorMessages.get_context_data(self, **kwargs)
		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs['list_of_events'] = self.listOfEvents
		kwargs['list_of_variables'] = [var.getNameOrSbmlId() for var in self.listOfVariables]
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
				self.delete(request)

			elif request.POST['action'] == "save":
				self.save(request)

		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasErrorMessages.clearErrors(self)
		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.listOfEvents = self.getModel().listOfEvents.values()
			self.getModel().listOfVariables.classifyVariables()

			self.listOfVariables = []
			for variable in self.getModel().listOfVariables.values():
				if ((variable.isParameter() and variable.isGlobal())
					or variable.isSpecies()
					or variable.isCompartment()
					or variable.isStoichiometry()):
					self.listOfVariables.append(variable)

	def delete(self, request):

		if (request.POST.get('event_id') is not None
			and str(request.POST['event_id']).isdigit()):

			t_id = int(request.POST['event_id'])
			if t_id < len(self.listOfEvents):
				try:
					self.getModel().listOfEvents.remove(self.listOfEvents[t_id])

				except ModelException as e:
					self.form.addError(e.message)

				self.saveModel(request)
				self.listOfEvents = self.getModel().listOfEvents.values()

	def save(self, request):

		self.form.read(request)
		if not self.form.hasErrors():

			if self.form.isNew():
				t_event = self.getModel().listOfEvents.new()
				self.form.save(t_event)

			else:
				t_event = self.getModel().listOfEvents[self.listOfEvents[self.form.id].objId]
				self.form.save(t_event)

			self.saveModel(request)
			self.listOfEvents = self.getModel().listOfEvents.values()
			self.form.clear()

