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

""" GetListOfObjectsFromSubmodels.py

	This file...

"""

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel

from libsignetsim.model.Variable import Variable


class GetListOfObjectsFromSubmodels(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)


	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		self.data.update({'list': self.getListOfObjects(request)})

		return JsonRequest.post(self, request, *args, **kwargs)


	def getListOfObjects(self, request):

		if str(request.POST['model_id']) != "":
			submodel = self.getModel().listOfSubmodels[int(request.POST['model_id'])].getModelObject()

			self.listOfObjects = []
			for t_object in submodel.listOfSbmlObjects:
				if isinstance(t_object, Variable) and not t_object.isStoichiometry():
					self.listOfObjects.append(t_object.getNameOrSbmlId() + (" (%s)" % type(t_object).__name__))

			return self.listOfObjects
