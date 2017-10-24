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

""" HasWorkingProject.py

	This file ...

"""

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404

from signetsim.views.HasUserLoggedIn import HasUserLoggedIn
from signetsim.models import SbmlModel, Project

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

				# # If a model was selected, we forget it
				# if request.session.get('model_id') is not None:
				# 	del request.session['model_id']
				# 	if request.session.get('model_submodel') is not None:
				# 		del request.session['model_submodel']

			else:
				raise PermissionDenied
		else:
			raise Http404("Project doesn't exists")

	def __setProject(self, request):

		t_project_id = self.listOfProjects[int(request.POST['project_id'])].folder
		self.setProject(request, t_project_id)


	def __loadProject(self, request, *args):

		if request.session.get('project_id') is not None:
			self.project_id = int(request.session['project_id'])

		if self.project_id is not None and Project.objects.filter(id=self.project_id).exists():
			self.project = Project.objects.get(id=self.project_id)
			self.project_name = self.project.name
		elif len(Project.objects.filter(access=Project.PUBLIC)) > 0:
			self.project = Project.objects.filter(access=Project.PUBLIC)[0]
			self.project_name = self.project.name
			self.project_id = self.project.id


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
		else:
			return []

	def isProjectOwner(self, request):
		return self.isUserLoggedIn(request) and self.project is not None and self.project.user == request.user

	def isProjectPublic(self):
		return self.project is not None and self.project.access == "PU"