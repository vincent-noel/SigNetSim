#!/usr/bin/env python
""" ListOfProjectsView.py


	This file generates the view for the list of models


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
from signetsim.views.HasWorkingProject import HasWorkingProject
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File

from signetsim.models import Project, SbmlModel#, FittedSbmlModel
from signetsim.models import Optimization, ContinuationComputation
from signetsim.models import Experiment, Condition, Observation, Treatment

from signetsim.forms import DocumentForm

from libsignetsim.model.Model import Model
from libsignetsim.model.ModelException import ModelException

from os.path import join, isfile, isdir, basename
from os import remove, mkdir
from shutil import rmtree, copy

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

			elif request.POST['action'] == "new_folder":
				self.newFolder(request)

			elif request.POST['action'] == "copy_folder":
				self.copyFolder(request)

			elif request.POST['action'] == "delete_folder":
				self.deleteFolder(request)

			elif request.POST['action'] == "send_folder":
				self.sendFolder(request)

		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)
		if self.isUserLoggedIn(request):
			self.loadFolders(request)

	def newFolder(self, request):

		folder_name = str(request.POST['folder_name'])

		if not Project.objects.filter(user=request.user, name=folder_name).exists():
			new_folder = Project(user=request.user, name=folder_name)
			new_folder.save()
			mkdir(join(settings.MEDIA_ROOT, str(new_folder.folder)))

			self.loadFolders(request)
		else:
			self.createFolderShow = True
			self.createFolderError = "Project %s already exists !" % folder_name

	def copyFolder(self, request):

		folder_id = str(request.POST['id'])
		if Project.objects.filter(user=request.user, id=folder_id).exists():

			folder = Project.objects.get(user=request.user, id=folder_id)
			new_folder = Project(user=request.user, name=(str(folder.name) + " (Copy)"))

			self.copyProjectModels(folder, new_folder)
			self.copyProjectExperiments(folder, new_folder)

			new_folder.save()


	def deleteFolder(self, request):

		folder_id = str(request.POST['id'])

		if self.project_id == int(folder_id):
			self.unsetProject(request)

		if Project.objects.filter(user=request.user, id=folder_id).exists():

			project = Project.objects.get(user=request.user, id=folder_id)

			self.__deleteProjectModels(project)
			self.__deleteProjectData(project)
			self.__deleteProjectOptimizations(project)
			self.__deleteProjectEquilibriumCurve(project)

			if isdir(join(settings.MEDIA_ROOT, str(project.folder))):
				rmtree(join(settings.MEDIA_ROOT, str(project.folder)))
			project.delete()


	def __deleteProjectModels(self, project):

		for model in SbmlModel.objects.filter(project=project):
			filename = join(settings.MEDIA_ROOT, str(model.sbml_file))
			if isfile(filename):
				remove(filename)
			model.delete()


		# for fitted_model in FittedSbmlModel.objects.filter(project=project):
		#     filename = join(settings.MEDIA_ROOT, str(fitted_model.sbml_file))
		#     if isfile(filename):
		#         remove(filename)
		#     fitted_model.delete()


	def __deleteProjectData(self, project):


		for experiment in Experiment.objects.filter(project=project):
			for condition in Condition.objects.filter(experiment=experiment):
				for observation in Observation.objects.filter(condition=condition):
					observation.delete()
				for treatment in Treatment.objects.filter(condition=condition):
					treatment.delete()
				condition.delete()
			experiment.delete()


	def __deleteProjectOptimizations(self, project):

		for optim in Optimization.objects.filter(project=project):
			subdirectory = "optimization_%s" % optim.optimization_id
			directory = join(settings.MEDIA_ROOT, project.folder, "optimizations", subdirectory)
			if isdir(directory):
				rmtree(directory)
			optim.delete()


	def __deleteProjectEquilibriumCurve(self, project):

		for cont in ContinuationComputation.objects.filter(project=project):
			cont.delete()


	def copyProjectModels(self, project, new_project):

		t_models = SbmlModel.objects.filter(project=project)
		for model in t_models:
			t_file = File(open(join(settings.MEDIA_ROOT, str(model.sbml_file))))

			new_model = SbmlModel(project=new_project, name=model.name,
									sbml_file=t_file)
			new_model.save()

	def copyProjectExperiments(self, project, new_project):

		t_experiments = Experiment.objects.filter(project=project)
		for experiment in t_experiments:

			new_experiment = Experiment(project=new_project,
											name=str(experiment.name),
											notes=str(experiment.notes))

			t_conditions = Condition.objects.filter(experiment=experiment)
			for condition in t_conditions:
				new_condition = Condition(experiment=new_experiment,
											name=str(condition.name),
											notes=str(condition.notes))


				t_observations = Observation.objects.filter(condition=condition)
				for t_observation in t_observations:
					new_observation = Observation(condition=new_condition,
										species=t_observation.species,
										time=t_observation.time,
										value=t_observation.value,
										stddev=t_observation.stddev,
										steady_state=t_observation.steady_state,
										min_steady_state=t_observation.min_steady_state,
										max_steady_state=t_observation.max_steady_state)

					new_observation.save()

				t_treatments = Treatment.objects.filter(condition=condition)
				for t_treatment in t_treatments:
					new_treatment = Treatment(condition=new_condition,
										species=t_treatment.species,
										time=t_treatment.time,
										value=t_treatment.value)

					new_treatment.save()

				new_condition.save()
			new_experiment.save()


	def sendFolder(self, request):

		folder_id = str(request.POST['id'])
		# print "Folder %s" % folder_id
		t_username = str(request.POST['username'])
		try :
			t_user = User.objects.get(username=t_username)
			if Project.objects.filter(user=request.user, id=folder_id).exists():

				folder = Project.objects.get(user=request.user, id=folder_id)
				new_folder = Project(user=t_user, name=str(folder.name))

				self.copyProjectModels(folder, new_folder)
				self.copyProjectExperiments(folder, new_folder)

				new_folder.save()




		except User.DoesNotExist:
			self.sendFolderShow = True
			self.sendFolderError = "Username %s does not exist" % t_username



	def loadFolders(self, request):
		self.listOfFolders = Project.objects.filter(user=request.user)
