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

""" GetListOfObjects.py

	This file...

"""

from django.conf import settings
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.model.Variable import Variable
from os.path import join

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class GetListOfObjects(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)


	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		t_list = self.getListOfObjects(request)
		self.data.update({'list': t_list})

		return JsonRequest.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)


	def getListOfObjects(self, request):

		if str(request.POST['model_id']) != "":
			list_of_project_models = [pm for pm in self.getProjectModels(request) if pm.id != self.model_id]

			t_model = list_of_project_models[int(request.POST['model_id'])]
			t_filename = join(settings.MEDIA_ROOT, str(t_model.sbml_file))
			doc = SbmlDocument()
			doc.readSbmlFromFile(t_filename)

			if (
				'submodel_id' in request.POST
				and request.POST['submodel_id'] != ""
				and int(request.POST['submodel_id']) > 1
			):

				submodel = doc.model.listOfSubmodels.values()[int(request.POST['submodel_id'])-1].getModelObject()
				self.listOfObjects = []
				for t_object in doc.model.listOfSbmlObjects.values():
					if isinstance(t_object, Variable) and not t_object.isStoichiometry():
						self.listOfObjects.append(t_object.getNameOrSbmlId() + (" (%s)" % type(t_object).__name__))

				return self.listOfObjects

			else:
				self.listOfObjects = []
				for t_object in doc.model.listOfSbmlObjects.values():
					if isinstance(t_object, Variable) and not t_object.isStoichiometry():
						self.listOfObjects.append(t_object.getNameOrSbmlId() + (" (%s)" % type(t_object).__name__))

				return self.listOfObjects
