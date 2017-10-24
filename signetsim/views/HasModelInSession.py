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
		# print "> Unpickling"
		return cloudpickle.loads(self.__request.session['loaded_model_doc']).model

	def getModelIdFromSession(self):
		return self.__request.session.get('loaded_model_id')

	def saveModelInSession(self, model, model_id):
		# print "> Pickling"
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
				pass

	def saveSubmodelInSession(self, submodel_id):
		self.__request.session['loaded_model_submodel'] = submodel_id

	def deleteSubmodelFromSession(self):
		if self.hasSubmodelInSession():
			del self.__request.session['loaded_model_submodel']
