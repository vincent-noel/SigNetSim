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

""" DataView.py

	This file ...

"""

from django.views.generic import TemplateView
from signetsim.views.HasWorkingProject import HasWorkingProject
from signetsim.forms import DocumentForm
from signetsim.models import Experiment
from signetsim.managers.data import importExperiment as importExperimentViaManager
from signetsim.managers.data import copyExperiment as copyExperimentViaManager
from signetsim.managers.data import deleteExperiment as deleteExperimentViaManager
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from os.path import join
from os import remove

class DataView(TemplateView, HasWorkingProject):

	template_name = 'data/data.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingProject.__init__(self)

		self.listOfExperiments = None
		self.experimentId = None
		self.experimentName = None
		self.experimentNotes = None
		self.fileUploadForm = DocumentForm()


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingProject.get_context_data(self, **kwargs)

		kwargs['experimental_data'] = self.listOfExperiments
		kwargs['experiment_id'] = self.experimentId
		kwargs['experiment_name'] = self.experimentName
		kwargs['experiment_notes'] = self.experimentNotes
		kwargs['file_upload_form'] = self.fileUploadForm
		return kwargs


	def get(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)
		self.loadExperiments(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)
		self.loadExperiments(request)

		if "action" in request.POST:

			if HasWorkingProject.isChooseProject(self, request):
				self.loadExperiments(request)

			elif request.POST['action'] == "delete":
				self.deleteExperiment(request)

			elif request.POST['action'] == "save":
				self.saveExperiment(request)

			elif request.POST['action'] == "duplicate":
				self.duplicateExperiment(request)

			elif request.POST['action'] == "import":
				self.importExperiment(request)

		return TemplateView.get(self, request, *args, **kwargs)


	def loadExperiments(self, request):
		self.listOfExperiments = Experiment.objects.filter(project=self.project)


	def deleteExperiment(self, request):

		if self.isProjectOwner(request):

			experiment = Experiment.objects.get(project=self.project,
												id=request.POST['id'])

			deleteExperimentViaManager(experiment)

	def saveExperiment(self, request):

		if self.isProjectOwner(request):
			if str(request.POST['experiment_id']) == "":
				t_experiment = Experiment(project=self.project)
			else:
				t_experiment = Experiment.objects.get(project=self.project, id=str(request.POST['experiment_id']))

			t_experiment.name = str(request.POST['experiment_name'])
			t_experiment.notes = str(request.POST['experiment_notes'])
			t_experiment.save()


	def duplicateExperiment(self, request):

		if self.isProjectOwner(request):

			t_experiment = Experiment.objects.get(project=self.project,
												  id=request.POST['id'])

			new_experiment = Experiment(project=self.project)
			new_experiment.save()
			copyExperimentViaManager(t_experiment, new_experiment)


	def importExperiment(self, request):

		if self.isProjectOwner(request):

			self.fileUploadForm = DocumentForm(request.POST, request.FILES)
			if self.fileUploadForm.is_valid():

				new_experiment = Experiment(project=self.project)
				new_experiment.save()

				archive = request.FILES['docfile']
				path = default_storage.save(str(archive), ContentFile(archive.read()))
				importExperimentViaManager(new_experiment, str(join(settings.MEDIA_ROOT, path)))
				remove(join(settings.MEDIA_ROOT, path))
