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

""" ListOfModelsView.py

	This file generates the view for the list of models

"""

from django.views.generic import TemplateView
from signetsim.views.HasWorkingProject import HasWorkingProject
from signetsim.views.HasUserLoggedIn import HasUserLoggedIn
from signetsim.views.HasErrorMessages import HasErrorMessages

from django.core.files import File
from django.conf import settings
from django.shortcuts import redirect

from signetsim.models import SbmlModel, new_model_filename
from signetsim.forms import DocumentForm

from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.model.ModelException import ModelException, MissingSubmodelException

import os


class ListOfModelsView(TemplateView, HasWorkingProject, HasUserLoggedIn, HasErrorMessages):

	template_name = 'models/models.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingProject.__init__(self)
		HasUserLoggedIn.__init__(self)
		HasErrorMessages.__init__(self)

		self.listOfModels = None
		self.fileUploadForm = DocumentForm()


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingProject.get_context_data(self, **kwargs)
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)

		kwargs['form'] = self.fileUploadForm
		kwargs['sbml_models'] = self.listOfModels

		return kwargs


	def get(self, request, *args, **kwargs):

		if len(args) > 0:
			HasWorkingProject.load(self, request, *args, **kwargs)
			self.setProject(request, args[0])
			return redirect('models')

		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingProject.isChooseProject(self, request):
				self.loadModels(request)

			elif request.POST['action'] == "delete_model":
				self.deleteModel(request)
				self.load(request, *args, **kwargs)


			elif request.POST['action'] == "load_model":
				self.loadModel(request)
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "duplicate_model":
				self.duplicateModel(request)
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "new_model":
				self.newModel(request)
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "load_biomodels":
				self.loadBiomodels(request)
				self.load(request, *args, **kwargs)


		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)

		self.loadModels(request)

	def newModel(self, request):

		model_name = str(request.POST['model_name'])
		model_filename = os.path.join(settings.MEDIA_ROOT, new_model_filename())

		open(model_filename,"a")
		new_model = SbmlModel(project=self.project, name=model_name, sbml_file=File(open(model_filename,"r")))
		os.remove(model_filename)
		new_model.save()

		doc = SbmlDocument()
		doc.model.newModel(model_name)
		doc.writeSbmlToFile(os.path.join(settings.MEDIA_ROOT, str(new_model.sbml_file)))


	def duplicateModel(self, request):

		model = SbmlModel.objects.get(id=request.POST['id'])
		t_file = File(open(os.path.join(settings.MEDIA_ROOT, str(model.sbml_file)) ))

		new_sbml_model = SbmlModel(project=self.project,
										name=("%s (copy)" % str(model.name)),
										sbml_file=t_file)

		new_sbml_model.save()
		t_filename = os.path.join(settings.MEDIA_ROOT, str(new_sbml_model.sbml_file))

		doc = SbmlDocument()
		doc.readSbmlFromFile(t_filename)
		doc.model.setName(str(new_sbml_model.name))
		doc.writeSbmlToFile(t_filename)


	def loadModel(self, request):

		self.fileUploadForm = DocumentForm(request.POST, request.FILES)
		if self.fileUploadForm.is_valid():

			new_sbml_model = SbmlModel(project=self.project,
										sbml_file=request.FILES['docfile'])
			new_sbml_model.save()

			try:
				doc = SbmlDocument()
				doc.readSbmlFromFile(os.path.join(settings.MEDIA_ROOT,
											str(new_sbml_model.sbml_file)))

				new_sbml_model.name = doc.model.getName()
				new_sbml_model.save()

			except MissingSubmodelException:
				new_sbml_model.delete()
				self.addError(
					"This model is importing some models which were not found in the project folder. Please import them first")

			# Is triggered where name is None ??
			except ModelException:
				name = os.path.splitext(str(new_sbml_model.sbml_file))[0]
				new_sbml_model.name = name
				new_sbml_model.save()


	def deleteModel(self, request):

		model = SbmlModel.objects.get(project=self.project, id=request.POST['id'])
		os.remove(os.path.join(settings.MEDIA_ROOT, str(model.sbml_file)))
		model.delete()

	def loadBiomodels(self, request):

		model_id = str(request.POST['model_id'])
		model_filename = os.path.join(settings.MEDIA_ROOT, new_model_filename())

		open(model_filename, "a")
		new_model = SbmlModel(project=self.project, sbml_file=File(open(model_filename,"r")))
		os.remove(model_filename)
		new_model.save()


		doc = SbmlDocument()
		try:

			doc.readFromBiomodels(model_id)
			doc.writeSbmlToFile(os.path.join(settings.MEDIA_ROOT, str(new_model.sbml_file)))
			new_model.name = doc.model.getName()
			new_model.save()

		except:
			self.addError("Unable to load model from biomodels")
			new_model.delete()

	def loadModels(self, request, *args, **kwargs):

		# self.projectId = str(args[0])
		# self.project = ModelFolder.objects.get(user=request.user, id=self.projectId)
		if self.project is not None:
			self.listOfModels = []
			for model in SbmlModel.objects.filter(project=self.project):
				filename = str(model.sbml_file)
				if filename.startswith(settings.MEDIA_ROOT):
					filename = filename.replace(settings.MEDIA_ROOT, "")
				self.listOfModels.append((model.id, model.name, filename))