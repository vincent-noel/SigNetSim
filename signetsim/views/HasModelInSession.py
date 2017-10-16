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

""" HasWorkingModel.py

	This file ...

"""

from django.conf import settings
from django.core.exceptions import PermissionDenied

from signetsim.models import SbmlModel
from libsignetsim.model.SbmlDocument import SbmlDocument
from signetsim.views.HasWorkingProject import HasWorkingProject
import os
import cloudpickle
from libsbml import Date
import datetime

class HasModelInSession(object):

	def __init__(self):
		self.__request = None

	def load(self, request, *args, **kwargs):
		self.__request = request

	# Model
	def hasModelInSession(self):
		return (
			self.__request.session.get('loaded_model_doc') is not None
			and self.__request.session.get('loaded_model_id') is not None
		)

	def getModelFromSession(self):
		return cloudpickle.loads(self.__request.session['loaded_model_doc']).model

	def getModelIdFromSession(self):
		return self.__request.session.get('loaded_model_id')

	def saveModelInSession(self, model, model_id):
		self.model.cleanBeforePickle()
		self.__request.session['loaded_model_doc'] = cloudpickle.dumps(model.parentDoc)
		self.__request.session['loaded_model_id'] = model_id

	def deleteModelFromSession(self):
		if self.hasModelInSession():
			del self.__request.session['loaded_model_doc']
			del self.__request.session['loaded_model_id']

	def hasSubmodelInSession(self):
		return self.__request.session.get('loaded_model_submodel') is not None

	def getSubmodelIdFromSession(self):
		submodel_id = str(self.__request.session['loaded_model_submodel'])
		if submodel_id != "":
			try:
				return int(submodel_id)
			except:
				return None
		else:
			return None

	def saveSubmodelInSession(self, submodel_id):
		self.__request.session['loaded_model_submodel'] = submodel_id

	def deleteSubmodelFromSession(self):
		del self.__request.session['loaded_model_submodel']

	# Model instance
	def hasModelInstanceInSession(self):
		return self.__request.session.get('loaded_model_instance') is not None

	def getModelInstanceFromSession(self):
		return cloudpickle.loads(self.__request.session['loaded_model_instance'])

	def saveModelInstanceInSession(self, model_instance):
		self.__request.session['loaded_model_instance'] = cloudpickle.dumps(model_instance)

	def deleteModelInstanceFromSession(self):
		if self.hasModelInstanceInSession():
			del self.__request.session['loaded_model_instance']

	#
	#
	#
	# def setModel(self, request, model_id):
	# 	# print ">Switching to model !!!!!"
	# 	if model_id is not None:
	# 		self.model_id = model_id
	# 		self.model_submodel = None
	# 		self.modelInstance = None
	#
	# 	self.__loadModelVariables()
	# 	self.savePickledModel(request)
	# 	request.session['model_id'] = self.model_id
	# 	request.session['model_submodel'] = ""
	#
	#
	# def __setModel(self, request):
	#
	# 	# print ">Switching to model %d : %s" % (self.list_of_models[int(request.POST['model_id'])].id, self.list_of_models[int(request.POST['model_id'])].name)
	# 	self.model_id = self.list_of_models[int(request.POST['model_id'])].id
	# 	self.model_submodel = 0
	# 	self.modelInstance = None
	# 	self.__loadModelVariables()
	# 	self.savePickledModel(request)
	# 	request.session['model_id'] = self.model_id
	# 	request.session['model_submodel'] = self.model_submodel
	#
	# def __setSubmodel(self, request):
	#
	# 	t_id = str(request.POST['submodel_id'])
	#
	# 	if t_id != "":
	# 		self.model_submodel = int(t_id)
	# 		if (self.model_submodel) > len(self.model.parentDoc.listOfModelDefinitions):
	# 			self.model_submodel = -1
	#
	# 	else:
	# 		self.model_submodel = 0
	#
	# 	request.session['model_submodel'] = self.model_submodel
	#
	#
	# def __loadModels(self, request):
	# 	if self.isProjectLoaded():
	# 		self.list_of_models = SbmlModel.objects.filter(project=self.project_id)
	#
	#
	# def __loadModel(self, request, *args):
	# 	""" Load the model for this view
	# 		Here the model_id is the indice of the model in the list
	# 		and model.id is the database model's id
	#
	# 	"""
	#
	# 	# if there is a model_id in the session variable
	# 	if request.session.get('model_id') is not None and self.project_id is not None and SbmlModel.objects.filter(
	# 				project=self.project_id,
	# 				id=int(request.session.get('model_id'))).exists():
	#
	# 			self.model_id = int(request.session['model_id'])
	# 		# # Otherwise we just load the first one on the list
	# 		# elif self.list_of_models is not None and len(self.list_of_models) > 0:
	# 		# 		self.model_id = self.list_of_models[0].id
	# 		# else:
	# 		# 	raise PermissionDenied
	#
	# 	# Otherwise we just load the first one on the list, if there is a lists
	# 	elif self.list_of_models is not None and len(self.list_of_models) > 0:
	# 			self.model_id = self.list_of_models[0].id
	#
	# 	# else:
	# 	# 	raise PermissionDenied
	#
	# 	# Now that we have a model id, we look if we have a pickled model in memory
	# 	# If it's the same, all good,
	# 	if (self.model_id is not None
	# 			and request.session.get('loaded_model_id') is not None
	# 			and request.session.get('loaded_model_id') == self.model_id):
	#
	# 		request.session['model_id'] = self.model_id
	#
	# 		# Looking for the pickled model, if not None we load it
	# 		if request.session.get('loaded_model_doc') is not None:
	# 			self.__loadPickledModel(request)
	#
	# 		# Otherwise we have a problem, so we load the chosen model
	# 		# and otherwrite the pickled part
	# 		else:
	# 			self.__loadModelVariables()
	# 			self.savePickledModel(request)
	#
	# 	# Now if we don't have a pickled model in memory, we just have
	# 	# to load the model and write the pickled model
	# 	else:
	# 	#Finally, we load the choosed model (if there is one)
	# 		request.session['model_id'] = self.model_id
	# 		self.__loadModelVariables()
	# 		self.savePickledModel(request)
	#
	# 	if request.session.get('model_submodel') is not None:
	# 		t_submodel_id = str(request.session['model_submodel'])
	# 		if t_submodel_id != "":
	# 			self.model_submodel = int(t_submodel_id)
	# 		else:
	# 			self.model_submodel = None
	#
	#
	#
	# def __loadModelVariables(self):
	#
	# 	if self.model_id is not None and self.project_id is not None and SbmlModel.objects.filter(project=self.project_id, id=self.model_id).exists():
	#
	# 		t_model = SbmlModel.objects.get(project=self.project_id, id=self.model_id)
	# 		self.model_filename = os.path.join(settings.MEDIA_ROOT, str(t_model.sbml_file))
	#
	# 		t_doc = SbmlDocument()
	# 		t_doc.readSbmlFromFile(self.model_filename)
	# 		self.model = t_doc.model
	# 		self.model_name = self.model.getName()
	#
	# 		self.model_list_of_submodels = self.model.listOfSubmodels.values()
	# 		self.model_list_of_submodels_names = []
	# 		self.model_list_of_submodels_types = []
	# 		for submodel in self.model.listOfSubmodels.values():
	# 			if submodel.getModelRef() in self.model.parentDoc.listOfModelDefinitions.sbmlIds():
	# 				self.model_list_of_submodels_names.append(self.model.parentDoc.listOfModelDefinitions.getBySbmlId(submodel.getModelRef()).getNameOrSbmlId())
	# 				self.model_list_of_submodels_types.append(0)
	# 			if submodel.getModelRef() in self.model.parentDoc.listOfExternalModelDefinitions.sbmlIds():
	# 				self.model_list_of_submodels_names.append(self.model.parentDoc.listOfExternalModelDefinitions.getBySbmlId(submodel.getModelRef()).getNameOrSbmlId())
	# 				self.model_list_of_submodels_types.append(1)
	# 	else:
	# 		raise PermissionDenied
	#
	# def __clearModelVariables(self):
	#
	# 	self.model_id = None
	# 	self.model = None
	# 	self.model_name = None
	# 	self.model_submodel = None
	# 	self.modelInstance = None
	#
	# def savePickledInstance(self):
	#
	# 	if self.modelInstance is not None and self.__request is not None:
	# 		self.__request.session['loaded_model_instance'] = cloudpickle.dumps(self.modelInstance)
	#
	# def deletePickledInstance(self):
	#
	# 	if self.__request is not None and self.__request.session.get('loaded_model_instance') is not None:
	# 		del self.__request.session['loaded_model_instance']
	#

	#
	# def savePickledModel(self, request):
	#
	# 	if self.model_id is not None:
	# 		self.model.cleanBeforePickle()
	#
	# 		request.session['loaded_model_id'] = self.model_id
	# 		request.session['loaded_model_doc'] = cloudpickle.dumps(self.model.parentDoc)
	# 		request.session['loaded_model_submodel'] = self.model_submodel
	#
	# 		if self.model_filename is None:
	# 			if SbmlModel.objects.filter(id=self.model_id).exists():
	# 				t_model = SbmlModel.objects.get(id=self.model_id)
	# 				self.model_filename = t_model.sbml_file
	#
	# 		request.session['loaded_model_filename'] = self.model_filename
	#
	#
	# def __loadPickledModel(self, request):
	# 	# t0 = time.time()
	# 	# print request.session.get('loaded_model_doc')
	# 	t_doc = cloudpickle.loads(request.session.get('loaded_model_doc'))
	# 	# print "> loaded pickled model in %.2gs" % (time.time()-t0)
	# 	self.model = t_doc.model
	# 	self.model_submodel = request.session['loaded_model_submodel']
	# 	self.model_name = self.model.getName()
	# 	self.model_filename = str(request.session['loaded_model_filename'])
	#
	# def __clearPickledModel(self, request):
	#
	# 	del request.session['loaded_model_id']
	# 	del request.session['loaded_model_doc']
	# 	del request.session['loaded_model_submodel']
	# 	del request.session['loaded_model_filename']
	# 	del request.session['loaded_model_instance']
	#
	# def getModelSubmodels(self, request, model_id):
	# 	""" Returning the submodels of a model available within the project
	# 	"""
	# 	if self.isUserLoggedIn(request) and self.project is not None:
	# 		t_models = [pm for pm in self.getProjectModels(request) if pm.id != self.model_id]
	# 		t_filename = os.path.join(settings.MEDIA_ROOT, str(t_models[model_id].sbml_file))
	# 		doc = SbmlDocument()
	# 		doc.readSbmlFromFile(t_filename)
	# 		if doc.useCompPackage:
	# 			return [doc.model.getSbmlId()] + doc.listOfModelDefinitions.sbmlIds()+doc.listOfExternalModelDefinitions.sbmlIds()
	# 		else:
	# 			return [doc.model.getSbmlId()]
	#
	# def getModelSBMLSubmodels(self, request):
	# 	""" Returning the submodels of a model available within the project
	# 	"""
	# 	if self.isUserLoggedIn(request) and self.project is not None and self.model_id is not None:
	# 		t_filename = os.path.join(settings.MEDIA_ROOT, str(self.model_filename))
	# 		doc = SbmlDocument()
	# 		doc.readSbmlFromFile(t_filename)
	# 		if doc.useCompPackage:
	# 			return (doc.listOfModelDefinitions.getListOfModelDefinitions()
	# 					+doc.listOfExternalModelDefinitions.getListOfModelDefinitions())
