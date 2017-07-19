#!/usr/bin/env python
""" HasWorkingModel.py


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

from signetsim.models import SbmlModel
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.model.Model import Model
# from libsignetsim.model.ModelException import ModelException
from signetsim.views.HasWorkingProject import HasWorkingProject
import os
import time
import pickle
import codecs
# from sbml_diff import generate_dot, sbml_diff
import sys
from libsbml import Date
import datetime

class HasWorkingModel(HasWorkingProject):

	def __init__(self):

		HasWorkingProject.__init__(self)

		self.list_of_models = None

		self.model = None
		self.modelInstance = None
		self.model_id = None
		self.model_name = None
		self.model_filename = None
		self.model_list_of_submodels = []
		self.model_list_of_submodels_names = []
		self.model_list_of_submodels_types = []
		self.model_submodel = None


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingProject.get_context_data(self, **kwargs)

		kwargs['sbml_models'] = self.list_of_models
		kwargs['model_id'] = self.model_id
		kwargs['model_name'] = self.model_name
		kwargs['model_has_submodels'] = (self.model is not None and self.model.parentDoc.isCompEnabled() and len(self.model.listOfSubmodels) > 0)
		kwargs['model_submodels'] = ["Model definition"] + [model.getName() for model in self.model.parentDoc.listOfModelDefinitions.values()]
		kwargs['model_submodel'] = self.model_submodel

		return kwargs


	def load(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)
		self.__loadModels(request)
		self.__loadModel(request, *args)


	def isChooseModel(self, request):

		if HasWorkingProject.isChooseProject(self, request):

			self.list_of_models = None
			self.__clearModelVariables()
			self.__clearPickledModel(request)
			return True

		elif request.POST['action'] == "choose_model":
			self.__setModel(request)
			return True

		elif request.POST['action'] == "choose_submodel":
			self.__setSubmodel(request)
			return True

		else:
			return False

	def getModelInstance(self):
		if self.modelInstance is None and self.model is not None:
			self.modelInstance = self.model.parentDoc.getModelInstance()
		return self.modelInstance


	def getModel(self):

		if self.model_submodel is None or self.model_submodel == 0:
			return self.model
		elif self.model_submodel == -1:
			return self.getModelInstance()
		else:
			t_list_submodels = self.model.parentDoc.listOfModelDefinitions.values()
			return t_list_submodels[self.model_submodel-1].modelDefinition

	def saveModel(self, request):
		if self.model is not None:
			self.savePickledModel(request)
			if self.model_filename is not None:
				self.saveModelHistory(request)
				self.model.parentDoc.writeSbmlToFile(self.model_filename)


	def saveModelHistory(self, request):
		if self.model.sbmlLevel >= 2:


			creator = self.model.modelHistory.createCreator()
			if str(request.user.email) not in self.model.modelHistory.getListOfCreatorsEmails():
				creator = self.model.modelHistory.createCreator()
				creator.setGivenName(request.user.first_name.encode('utf-8'))
				creator.setEmail(request.user.email.encode('utf-8'))
				creator.setOrganization(request.user.organization.encode('utf-8'))
				creator.setFamilyName(request.user.last_name.encode('utf-8'))

			date = Date()
			now = datetime.datetime.now()
			date.setYear(now.year)
			date.setMonth(now.month)
			date.setDay(now.day)
			date.setHour(now.hour)
			date.setMinute(now.minute)
			date.setSecond(now.second)
			if self.model.modelHistory.getDateCreated() is None:
				self.model.modelHistory.setDateCreated(date)

			self.model.modelHistory.addModifiedDate(date)


	def reloadModel(self):
		self.__loadModelVariables()

	def isModelLoaded(self):
		return self.model is not None

	def isFlattenModel(self):
		return self.model_submodel is not None and self.model_submodel == -1

	def isCompModelDefinition(self):
		return self.model_submodel is not None and self.model_submodel == 0

	def isCompInternalSubmodel(self):
		return self.model_submodel is not None and self.model_submodel > 0

	def saveModelName(self, name):
		if self.model_submodel == 0:
			db_model = SbmlModel.objects.get(project=self.project_id, id=self.model_id)
			db_model.name = name
			db_model.save()


	def setModel(self, request, model_id):
		# print ">Switching to model !!!!!"
		if model_id is not None:
			self.model_id = model_id
			self.model_submodel = None
			self.modelInstance = None

		self.__loadModelVariables()
		self.savePickledModel(request)
		request.session['model_id'] = self.model_id
		request.session['model_submodel'] = ""


	def __setModel(self, request):

		# print ">Switching to model %d : %s" % (self.list_of_models[int(request.POST['model_id'])].id, self.list_of_models[int(request.POST['model_id'])].name)
		self.model_id = self.list_of_models[int(request.POST['model_id'])].id
		self.model_submodel = None
		self.modelInstance = None
		self.__loadModelVariables()
		self.savePickledModel(request)
		request.session['model_id'] = self.model_id
		request.session['model_submodel'] = self.model_submodel

	def __setSubmodel(self, request):

		t_id = str(request.POST['submodel_id'])

		if t_id != "":
			self.model_submodel = int(t_id)
			if (self.model_submodel) > len(self.model.parentDoc.listOfModelDefinitions):
				self.model_submodel = -1

		else:
			self.model_submodel = 0

		request.session['model_submodel'] = self.model_submodel


	def __loadModels(self, request):
		if self.isProjectLoaded():
			self.list_of_models = SbmlModel.objects.filter(project=self.project_id)


	def __loadModel(self, request, *args):
		""" Load the model for this view
			Here the model_id is the indice of the model in the list
			and model.id is the database model's id

		"""

		# if there is a model_id in the session variable
		if request.session.get('model_id') is not None:

			# If the model with that model_id actually exists, we load the model id
			if SbmlModel.objects.filter(
					project=self.project_id,
					id=int(request.session.get('model_id'))).exists():

				self.model_id = int(request.session['model_id'])

			# Otherwise we just load the first one on the list
			else:
				if self.list_of_models is not None and len(self.list_of_models) > 0:
					self.model_id = self.list_of_models[0].id

		# Otherwise we just load the first one on the list
		else:
			if self.list_of_models is not None and len(self.list_of_models) > 0:
				self.model_id = self.list_of_models[0].id



		# Now that we have a model id, we look if we have a pickled model in memory
		# If it's the same, all good,
		if (self.model_id is not None
				and request.session.get('loaded_model_id') is not None
				and request.session.get('loaded_model_id') == self.model_id):

			request.session['model_id'] = self.model_id

			# Looking for the pickled model, if not None we load it
			if request.session.get('loaded_model_doc') is not None:
				self.__loadPickledModel(request)

			# Otherwise we have a problem, so we load the chosen model
			# and otherwrite the pickled part
			else:
				self.__loadModelVariables()
				self.savePickledModel(request)

		# Now if we don't have a pickled model in memory, we just have
		# to load the model and write the pickled model
		else:
		#Finally, we load the choosed model (if there is one)
			request.session['model_id'] = self.model_id
			self.__loadModelVariables()
			self.savePickledModel(request)

		if request.session.get('model_submodel') is not None:
			t_submodel_id = str(request.session['model_submodel'])
			if t_submodel_id != "":
				self.model_submodel = int(t_submodel_id)
			else:
				self.model_submodel = None



	def __loadModelVariables(self):

		if self.model_id is not None:

			t_model = SbmlModel.objects.get(project=self.project_id, id=self.model_id)
			self.model_filename = os.path.join(settings.MEDIA_ROOT, str(t_model.sbml_file))

			t_doc = SbmlDocument()
			t_doc.readSbmlFromFile(self.model_filename)
			self.model = t_doc.model
			self.model_name = self.model.getName()

			self.model_list_of_submodels = self.model.listOfSubmodels.values()
			self.model_list_of_submodels_names = []
			self.model_list_of_submodels_types = []
			for submodel in self.model.listOfSubmodels.values():
				if submodel.getModelRef() in self.model.parentDoc.listOfModelDefinitions.sbmlIds():
					self.model_list_of_submodels_names.append(self.model.parentDoc.listOfModelDefinitions.getBySbmlId(submodel.getModelRef()).getNameOrSbmlId())
					self.model_list_of_submodels_types.append(0)
				if submodel.getModelRef() in self.model.parentDoc.listOfExternalModelDefinitions.sbmlIds():
					self.model_list_of_submodels_names.append(self.model.parentDoc.listOfExternalModelDefinitions.getBySbmlId(submodel.getModelRef()).getNameOrSbmlId())
					self.model_list_of_submodels_types.append(1)


	def __clearModelVariables(self):

		self.model_id = None
		self.model = None
		self.model_name = None
		self.model_submodel = None
		self.modelInstance = None



	def savePickledModel(self, request):

		if self.model_id is not None:
			self.model.cleanBeforePickle()

			request.session['loaded_model_id'] = self.model_id
			request.session['loaded_model_doc'] = pickle.dumps(self.model.parentDoc)
			request.session['loaded_model_submodel'] = self.model_submodel

			if self.model_filename is None:
				if SbmlModel.objects.filter(id=self.model_id).exists():
					t_model = SbmlModel.objects.get(id=self.model_id)
					self.model_filename = t_model.sbml_file

			request.session['loaded_model_filename'] = self.model_filename


	def __loadPickledModel(self, request):
		# t0 = time.time()
		# print request.session.get('loaded_model_doc')
		t_doc = pickle.loads(request.session.get('loaded_model_doc'))
		# print "> loaded pickled model in %.2gs" % (time.time()-t0)
		self.model = t_doc.model
		self.model_submodel = request.session['loaded_model_submodel']
		self.model_name = self.model.getName()
		self.model_filename = str(request.session['loaded_model_filename'])

	def __clearPickledModel(self, request):

		del request.session['loaded_model_id']
		del request.session['loaded_model_doc']
		del request.session['loaded_model_submodel']
		del request.session['loaded_model_filename']


	def getModelSubmodels(self, request, model_id):
		""" Returning the submodels of a model available within the project
		"""
		if self.isUserLoggedIn(request) and self.project is not None:
			t_models = [pm for pm in self.getProjectModels(request) if pm.id != self.model_id]
			t_filename = os.path.join(settings.MEDIA_ROOT, str(t_models[model_id].sbml_file))
			doc = SbmlDocument()
			doc.readSbmlFromFile(t_filename)
			if doc.useCompPackage:
				return [doc.model.getSbmlId()] + doc.listOfModelDefinitions.sbmlIds()+doc.listOfExternalModelDefinitions.sbmlIds()
			else:
				return [doc.model.getSbmlId()]

	def getModelSBMLSubmodels(self, request):
		""" Returning the submodels of a model available within the project
		"""
		if self.isUserLoggedIn(request) and self.project is not None and self.model_id is not None:
			t_filename = os.path.join(settings.MEDIA_ROOT, str(self.model_filename))
			doc = SbmlDocument()
			doc.readSbmlFromFile(t_filename)
			if doc.useCompPackage:
				return (doc.listOfModelDefinitions.getListOfModelDefinitions()
						+doc.listOfExternalModelDefinitions.getListOfModelDefinitions())
