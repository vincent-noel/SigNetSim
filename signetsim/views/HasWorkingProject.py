#!/usr/bin/env python
""" HasWorkingProject.py


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

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from signetsim.views.HasUserLoggedIn import HasUserLoggedIn

from signetsim.models import SbmlModel, Project

from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.model.Model import Model
from libsignetsim.model.ModelException import ModelException
import os

class HasWorkingProject(HasUserLoggedIn):

	def __init__(self):

		HasUserLoggedIn.__init__(self)

		self.listOfProjects = None
		self.project = None
		self.project_id = None
		self.project_name = None


	def get_context_data(self, **kwargs):

		kwargs['projects'] = self.listOfProjects
		kwargs['project_id'] = self.project_id
		kwargs['project_name'] = self.project_name

		return kwargs


	def load(self, request, *args, **kwargs):

		self.__loadProjects(request)
		self.__loadProject(request, *args)


	def isChooseProject(self, request):

		if request.POST['action'] == "choose_project":
			self.__setProject(request)
			return True

		elif request.POST['action'] == "new_project":
			self.__newProject(request)
			return True

		else:
			return False


	def isProjectLoaded(self):
		return (self.project_id != None and self.project != None)


	def setProject(self, request, project_folder):

		if Project.objects.filter(folder=str(project_folder)).exists():

			t_project = Project.objects.get(folder=str(project_folder))
			if t_project.user == request.user or t_project.access == Project.PUBLIC:
				self.project_id = t_project.id

				request.session['project_id'] = self.project_id
				self.__loadProject(request)

				# If a model was selected, we forget it
				if request.session.get('model_id') is not None:
					del request.session['model_id']
					if request.session.get('model_submodel') is not None:
						del request.session['model_submodel']


	def unsetProject(self, request):

		self.project_id = None
		self.project_name = None
		self.project = None
		del request.session['project_id']


	def __newProject(self, request):
		folder_name = str(request.POST['project_name'])

		if not Project.objects.filter(user=request.user, name=folder_name).exists():
			self.project = Project(user=request.user, name=folder_name)
			self.project.save()
			self.project_id = self.project.id
			self.project_name = self.project.name

			request.session['project_id'] = self.project_id
			os.mkdir(os.path.join(settings.MEDIA_ROOT, str(self.project.id)))
			os.mkdir(os.path.join(settings.MEDIA_ROOT, str(self.project.id), "optimizations"))
		else:
			self.createFolderShow = True
			self.createFolderError = "Project %s already exists !" % folder_name


		self.__loadProjects(request)

	def __setProject(self, request):

		t_project_id = self.listOfProjects[int(request.POST['project_id'])].folder
		self.setProject(request, t_project_id)


	def __loadProject(self, request, *args):

		if request.session.get('project_id') is not None:
			self.project_id = int(request.session['project_id'])

		if self.project_id is not None and Project.objects.filter(id=self.project_id).exists():
			self.project = Project.objects.get(id=self.project_id)
			self.project_name = self.project.name


	def __loadProjects(self, request):
		if self.isUserLoggedIn(request):
			self.listOfProjects = (Project.objects.filter(user=request.user)
									| Project.objects.filter(access=Project.PUBLIC))

		else:
			self.listOfProjects = Project.objects.filter(access=Project.PUBLIC)


	def getProjectFolder(self):
		if self.project is not None:
			return os.path.join(settings.MEDIA_ROOT, str(self.project.folder))

	def getProjectModels(self, request):
		if self.isUserLoggedIn(request) and self.project is not None:
			return SbmlModel.objects.filter(project=self.project)
