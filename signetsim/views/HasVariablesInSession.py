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

""" HasModelInSession.py

	This file 

"""

from signetsim.models import SbmlModel
from django.conf import settings
from os.path import join
import cloudpickle


class HasVariablesInSession(object):

	def __init__(self):
		self.__request = None

	def load(self, request, *args, **kwargs):
		self.__request = request

	# Project
	def hasProjectInSession(self):
		return self.__request.session.get('project_id') is not None

	def getProjectFromSession(self):
		return self.__request.session.get('project_id')

	def saveProjectInSession(self, project_id):
		self.__request.session['project_id'] = project_id
		self.deleteModelFromSession()

	def deleteProjectFromSession(self):
		if self.hasProjectInSession():
			del self.__request.session['project_id']
			self.deleteModelFromSession()

	# Model
	def hasModelInSession(self):
		return (
			self.__request.session.get('loaded_model_doc') is not None
			and self.__request.session.get('loaded_model_id') is not None
			and self.__request.session.get('loaded_model_filename') is not None
		)

	def getModelFromSession(self):
		# print("> Unpickling")
		return cloudpickle.loads(self.__request.session['loaded_model_doc']).model

	def getModelIdFromSession(self):
		return self.__request.session.get('loaded_model_id')

	def getModelFilenameFromSession(self):
		return self.__request.session.get('loaded_model_filename')

	def saveModelInSession(self, model, model_id):
		# print("> Pickling")
		self.model.cleanBeforePickle()
		self.__request.session['loaded_model_doc'] = cloudpickle.dumps(model.parentDoc)
		self.__request.session['loaded_model_id'] = model_id
		self.__request.session['loaded_model_filename'] = join(settings.MEDIA_ROOT,str(SbmlModel.objects.get(id=model_id).sbml_file))

	def deleteModelFromSession(self):
		if self.hasModelInSession():
			del self.__request.session['loaded_model_doc']
			del self.__request.session['loaded_model_id']
			del self.__request.session['loaded_model_filename']
			if self.hasSubmodelInSession():
				self.deleteSubmodelFromSession()

	def hasSubmodelInSession(self):
		return self.__request.session.get('loaded_model_submodel') is not None

	def getSubmodelIdFromSession(self):
		submodel_id = str(self.__request.session['loaded_model_submodel'])
		if submodel_id != "":
			try:
				return int(submodel_id)
			except:
				pass

	def saveSubmodelInSession(self, submodel_id):
		self.__request.session['loaded_model_submodel'] = submodel_id

	def deleteSubmodelFromSession(self):
		if self.hasSubmodelInSession():
			del self.__request.session['loaded_model_submodel']
