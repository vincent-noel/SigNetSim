#!/usr/bin/env python
""" GetListOfObjectsFromSubmodels.py


	This file...



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
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.model.Variable import Variable
from os.path import join

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class GetListOfObjectsFromSubmodels(JsonRequest, HasWorkingModel):

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
			list_of_project_models = self.getModelSBMLSubmodels(request)
			doc = list_of_project_models[int(request.POST['model_id'])]

			self.listOfObjects = []
			for t_object in doc.model.listOfSbmlObjects.values():
				if isinstance(t_object, Variable) and not t_object.isStoichiometry():
					self.listOfObjects.append(t_object.getNameOrSbmlId() + (" (%s)" % type(t_object).__name__))

			# print self.listOfObjects
			return self.listOfObjects
