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

""" ListOfProjectsView.py

	This file generates the view for the list of models

"""

from django.views.generic import TemplateView
from signetsim.views.HasWorkingProject import HasWorkingProject
from django.conf import settings
from signetsim.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from signetsim.models import Project
from signetsim.managers.projects import deleteProject, copyProject, importProject
from signetsim.forms import DocumentForm

from os.path import join, exists, isfile
from os import remove, mkdir


class ListOfProjectsView(TemplateView, HasWorkingProject):

	template_name = 'models/projects.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingProject.__init__(self)

		self.listOfFolders = None
		self.createFolderShow = None
		self.createFolderError = None
		self.sendFolderShow = None
		self.sendFolderError = None

	def get_context_data(self, **kwargs):

		kwargs = HasWorkingProject.get_context_data(self, **kwargs)

		kwargs['create_folder_error'] = self.createFolderError
		kwargs['create_folder_show'] = self.createFolderShow

		kwargs['send_folder_error'] = self.sendFolderError
		kwargs['send_folder_show'] = self.sendFolderShow
		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingProject.isChooseProject(self, request):
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "copy_folder":
				self.copyFolder(request)

			elif request.POST['action'] == "delete_folder":
				self.deleteFolder(request)

			elif request.POST['action'] == "send_folder":
				self.sendFolder(request)

			elif request.POST['action'] == "load_folder":
				self.loadFolder(request)

			elif request.POST['action'] == "save_project":
				self.saveProject(request)

		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)
		if self.isUserLoggedIn(request):
			self.loadFolders(request)

	def copyFolder(self, request):

		folder_id = str(request.POST['id'])
		if Project.objects.filter(id=folder_id).exists():

			folder = Project.objects.get(id=folder_id)
			new_folder = Project(user=request.user, name=(str(folder.name) + " (Copy)"))
			copyProject(folder, new_folder)


	def deleteFolder(self, request):

		folder_id = str(request.POST['id'])

		# if self.project_id == int(folder_id):
		# 	self.unsetProject(request)

		if Project.objects.filter(user=request.user, id=folder_id).exists():

			project = Project.objects.get(user=request.user, id=folder_id)
			deleteProject(project)


	def sendFolder(self, request):

		folder_id = str(request.POST['modal_send_project_id'])
		t_username = str(request.POST['modal_send_project_username'])
		try :
			t_user = User.objects.get(username=t_username)
			if Project.objects.filter(user=request.user, id=folder_id).exists():

				folder = Project.objects.get(user=request.user, id=folder_id)
				new_folder = Project(user=t_user, name=str(folder.name))
				copyProject(folder, new_folder)


		except User.DoesNotExist:
			self.sendFolderShow = True
			self.sendFolderError = "Username %s does not exist" % t_username

	def saveProject(self, request):

		if 'modal_project_name' in request.POST:
			if 'modal_project_id' in request.POST and request.POST['modal_project_id'] != "":
				id = request.POST['modal_project_id']
				name = request.POST['modal_project_name']
				access = False
				if 'modal_project_access' in request.POST and request.POST['modal_project_access'] == "on":
					access = True

				if Project.objects.filter(id=id).exists():
					project = Project.objects.get(id=id)
					project.name = name
					if access:
						project.access = 'PU'
					else:
						project.access = 'PR'
					project.save()

			else:

				name = str(request.POST['modal_project_name'])
				access = False
				if 'modal_project_access' in request.POST and request.POST['modal_project_access'] == "on":
					access = True

				if not Project.objects.filter(user=request.user, name=name).exists():
					new_folder = Project(user=request.user, name=name)
					if access:
						new_folder.access = 'PU'
					else:
						new_folder.access = 'PR'

					new_folder.save()
					mkdir(join(settings.MEDIA_ROOT, str(new_folder.folder)))

					self.loadFolders(request)
				else:
					self.createFolderShow = True
					self.createFolderError = "Project %s already exists !" % name

	def loadFolder(self, request):

		if 'combine_file' in request.FILES:

			try:
				new_folder = Project(user=request.user)

				archive = request.FILES['combine_file']
				path = join(settings.MEDIA_ROOT, str(archive))

				if exists(path):
					remove(path)

				t_content_file = open(path, "wb")
				t_content_file.write(archive.read())
				t_content_file.close()

				importProject(new_folder, path)

			except Exception as e:
				if isfile(path):
					remove(path)

			new_folder.save()

	def loadFolders(self, request):
		self.listOfFolders = Project.objects.filter(user=request.user)
