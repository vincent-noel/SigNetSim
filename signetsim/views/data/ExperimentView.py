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

""" ExperimentView.py

	This file ...

"""

from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.core.exceptions import PermissionDenied
from django.http import Http404

from signetsim.views.HasWorkingProject import HasWorkingProject
from signetsim.models import Experiment, Condition, Observation, Treatment
from signetsim.managers.data import copyCondition

class ExperimentView(TemplateView, HasWorkingProject):

	template_name = 'data/experiment.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingProject.__init__(self)

		self.experiment = None
		self.listOfConditions = None
		self.conditionId = None
		self.conditionName = None
		self.conditionNotes = None


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingProject.get_context_data(self, **kwargs)

		kwargs['experiment_name'] = self.experiment.name
		kwargs['conditions'] = self.listOfConditions

		kwargs['condition_id'] = self.conditionId
		kwargs['condition_name'] = self.conditionName
		kwargs['condition_notes'] = self.conditionNotes

		return kwargs


	def get(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)

		self.load(request, *args, **kwargs)

		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)

		self.load(request, *args, **kwargs)

		if "action" in request.POST:

			if HasWorkingProject.isChooseProject(self, request):
				return redirect('experimental_data')

			elif request.POST['action'] == "delete":
				self.deleteCondition(request)

			elif request.POST['action'] == "save":
				self.saveCondition(request)

			elif request.POST['action'] == "duplicate":
				self.duplicateCondition(request)

		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		self.loadExperiment(request, *args, **kwargs)
		self.loadConditions(request)


	def saveCondition(self, request):

		if str(request.POST['condition_id']) == "":
			condition = Condition(experiment=self.experiment)
		else:
			condition = Condition.objects.get(experiment=self.experiment, id=request.POST['condition_id'])

		condition.name = str(request.POST['condition_name'])
		condition.notes = str(request.POST['condition_notes'])
		condition.save()


	def deleteCondition(self, request):

		condition = Condition.objects.get(experiment=self.experiment, id=request.POST['id'])

		initial_data = Treatment.objects.filter(condition=condition)
		initial_data.delete()

		observed_data = Observation.objects.filter(condition=condition)
		observed_data.delete()

		condition.delete()


	def duplicateCondition(self, request):

		condition = Condition.objects.get(experiment=self.experiment, id=request.POST['id'])

		new_condition = Condition(experiment=self.experiment)
		new_condition.save()

		copyCondition(condition, new_condition)


	def loadConditions(self, request):

		self.listOfConditions = Condition.objects.filter(experiment=self.experiment)


	def loadExperiment(self, request, *args, **kwargs):

		if Experiment.objects.filter(id=args[0]).exists():
			self.experiment = Experiment.objects.get(id=args[0])
			if not (self.experiment.project.user == request.user or self.experiment.project.access == "PU"):
				raise PermissionDenied

		else:
			raise Http404("Experimental data doesn't exists !")
