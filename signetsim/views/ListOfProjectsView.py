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
from signetsim.models import User
from django.core.files import File

from signetsim.models import Project, SbmlModel, SEDMLSimulation, CombineArchiveModel
from signetsim.models import Optimization, ContinuationComputation
from signetsim.models import Experiment, Condition, Observation, Treatment
from signetsim.manager import deleteProject, copyProject
from signetsim.forms import DocumentForm
from libsignetsim.combine.CombineArchive import CombineArchive
from libsignetsim.combine.CombineException import CombineException
from libsignetsim.model.Model import Model
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.sedml.SedmlDocument import SedmlDocument
from libsignetsim.model.ModelException import ModelException

from os.path import join, isfile, isdir, basename, splitext
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
		self.fileUploadForm = DocumentForm()

	def get_context_data(self, **kwargs):

		kwargs = HasWorkingProject.get_context_data(self, **kwargs)

		kwargs['create_folder_error'] = self.createFolderError
		kwargs['create_folder_show'] = self.createFolderShow

		kwargs['send_folder_error'] = self.sendFolderError
		kwargs['send_folder_show'] = self.sendFolderShow
		kwargs['load_project_form'] = self.fileUploadForm
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

			elif request.POST['action'] == "load_folder":
				self.loadFolder(request)

			elif request.POST['action'] == "save_project":
				self.saveProject(request)

		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)
		if self.isUserLoggedIn(request):
			self.loadFolders(request)

	def newFolder(self, request):

		name = str(request.POST['project_name'])
		access = False
		if 'project_access' in request.POST and request.POST['project_access'] == "on":
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

	def copyFolder(self, request):

		folder_id = str(request.POST['id'])
		if Project.objects.filter(user=request.user, id=folder_id).exists():

			folder = Project.objects.get(user=request.user, id=folder_id)
			new_folder = Project(user=request.user, name=(str(folder.name) + " (Copy)"))
			copyProject(folder, new_folder)


	def deleteFolder(self, request):

		folder_id = str(request.POST['id'])

		if self.project_id == int(folder_id):
			self.unsetProject(request)

		if Project.objects.filter(user=request.user, id=folder_id).exists():

			project = Project.objects.get(user=request.user, id=folder_id)
			deleteProject(project)


	def sendFolder(self, request):

		folder_id = str(request.POST['id'])
		t_username = str(request.POST['username'])
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

		if 'project_name' in request.POST and 'project_id' in request.POST:
			if request.POST['project_id'] != "":
				id = request.POST['project_id']
				name = request.POST['project_name']
				access = False
				if 'project_access' in request.POST and request.POST['project_access'] == "on":
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
				self.newFolder(request)

	def loadFolder(self, request):

		self.fileUploadForm = DocumentForm(request.POST, request.FILES)
		if self.fileUploadForm.is_valid():

			new_folder = Project(user=request.user)
			new_folder.save()
			mkdir(join(settings.MEDIA_ROOT, str(new_folder.folder)))

			new_archive = CombineArchiveModel(project=new_folder, archive_file=request.FILES['docfile'])
			new_archive.save()

			new_combine_archive = CombineArchive()
			filename = join(settings.MEDIA_ROOT, str(new_archive.archive_file))
			t_name = basename(str(new_archive.archive_file))
			new_folder.name = t_name.split('.')[0]
			new_folder.save()

			try:
				new_combine_archive.readArchive(filename)

				for sbml_file in new_combine_archive.getAllSbmls():
					t_file = File(open(sbml_file, 'r'))

					sbml_model = SbmlModel(project=new_folder, sbml_file=t_file)
					sbml_model.save()

					try:
						doc = SbmlDocument()

						doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(sbml_model.sbml_file)))

						sbml_model.name = doc.model.getName()
						sbml_model.save()
					except ModelException:
						name = splitext(str(sbml_model.sbml_file))[0]
						sbml_model.name = name
						sbml_model.save()


				for sedml_filename in new_combine_archive.getAllSedmls():
					sedml_archive = SEDMLSimulation(project=new_folder, sedml_file=File(open(sedml_filename, 'r')))
					sedml_archive.name = basename(sedml_filename).split('.')[0]
					sedml_archive.save()

					# Now everything is in the same folder
					sedml_doc = SedmlDocument()
					sedml_doc.readSedmlFromFile(join(settings.MEDIA_ROOT, str(sedml_archive.sedml_file)))
					sedml_doc.listOfModels.removePaths()

					sbml_files = sedml_doc.listOfModels.makeLocalSources()

					for sbml_file in sbml_files:

						if len(SbmlModel.objects.filter(project=new_folder, sbml_file=join(join(str(new_folder.folder), "models"), basename(sbml_file)))) == 0:

							t_file = File(open(sbml_file, 'r'))
							sbml_model = SbmlModel(project=new_folder, sbml_file=t_file)
							sbml_model.save()
							try:
								doc = SbmlDocument()

								doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(sbml_model.sbml_file)))

								sbml_model.name = doc.model.getName()
								sbml_model.save()
							except ModelException:
								name = splitext(str(sbml_model.sbml_file))[0]
								sbml_model.name = name
								sbml_model.save()

					sedml_doc.writeSedmlToFile(join(settings.MEDIA_ROOT, str(sedml_archive.sedml_file)))



			except CombineException as e:
				print e.message

	def loadFolders(self, request):
		self.listOfFolders = Project.objects.filter(user=request.user)


	#
	# def __deleteProjectModels(self, project):
	#
	# 	for model in SbmlModel.objects.filter(project=project):
	# 		filename = join(settings.MEDIA_ROOT, str(model.sbml_file))
	# 		if isfile(filename):
	# 			remove(filename)
	# 		model.delete()
	#
	#
	#
	# def __deleteProjectData(self, project):
	#
	#
	# 	for experiment in Experiment.objects.filter(project=project):
	# 		for condition in Condition.objects.filter(experiment=experiment):
	# 			for observation in Observation.objects.filter(condition=condition):
	# 				observation.delete()
	# 			for treatment in Treatment.objects.filter(condition=condition):
	# 				treatment.delete()
	# 			condition.delete()
	# 		experiment.delete()
	#
	#
	# def __deleteProjectOptimizations(self, project):
	#
	# 	for optim in Optimization.objects.filter(project=project):
	# 		subdirectory = "optimization_%s" % optim.optimization_id
	# 		directory = join(settings.MEDIA_ROOT, project.folder, "optimizations", subdirectory)
	# 		if isdir(directory):
	# 			rmtree(directory)
	# 		optim.delete()
	#
	#
	# def __deleteProjectEquilibriumCurve(self, project):
	#
	# 	for cont in ContinuationComputation.objects.filter(project=project):
	# 		cont.delete()
	#
	#
	# def __deleteProjectArchives(self, project):
	#
	# 	for archive in CombineArchiveModel.objects.filter(project=project):
	# 		filename = join(settings.MEDIA_ROOT, str(archive.archive_file))
	# 		if isfile(filename):
	# 			remove(filename)
	# 		archive.delete()

	# def copyProjectModels(self, project, new_project):
	#
	# 	t_models = SbmlModel.objects.filter(project=project)
	# 	for model in t_models:
	# 		t_file = File(open(join(settings.MEDIA_ROOT, str(model.sbml_file))))
	#
	# 		new_model = SbmlModel(project=new_project, name=model.name,
	# 								sbml_file=t_file)
	# 		new_model.save()
	#
	# def copyProjectExperiments(self, project, new_project):
	#
	# 	t_experiments = Experiment.objects.filter(project=project)
	# 	for experiment in t_experiments:
	#
	# 		new_experiment = Experiment(project=new_project,
	# 										name=str(experiment.name),
	# 										notes=str(experiment.notes))
	# 		new_experiment.save()
	# 		t_conditions = Condition.objects.filter(experiment=experiment)
	# 		for condition in t_conditions:
	# 			new_condition = Condition(experiment=new_experiment,
	# 										name=str(condition.name),
	# 										notes=str(condition.notes))
	# 			new_condition.save()
	#
	# 			t_observations = Observation.objects.filter(condition=condition)
	# 			for t_observation in t_observations:
	# 				new_observation = Observation(condition=new_condition,
	# 									species=t_observation.species,
	# 									time=t_observation.time,
	# 									value=t_observation.value,
	# 									stddev=t_observation.stddev,
	# 									steady_state=t_observation.steady_state,
	# 									min_steady_state=t_observation.min_steady_state,
	# 									max_steady_state=t_observation.max_steady_state)
	#
	# 				new_observation.save()
	#
	# 			t_treatments = Treatment.objects.filter(condition=condition)
	# 			for t_treatment in t_treatments:
	# 				new_treatment = Treatment(condition=new_condition,
	# 									species=t_treatment.species,
	# 									time=t_treatment.time,
	# 									value=t_treatment.value)
	#
	# 				new_treatment.save()
	#
	# 			new_condition.save()
	# 		new_experiment.save()
