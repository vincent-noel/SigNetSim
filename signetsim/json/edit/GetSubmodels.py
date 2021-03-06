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

""" GetSubmodels.py

	This file...

"""

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class GetSubmodels(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)


	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		t_list = self.getSubmodelList(request)
		self.data.update({'list': t_list})

		return JsonRequest.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)


	def getSubmodelList(self, request):

		if str(request.POST['model_id']) != "":
			# print("model id = %d" % int(request.POST['model_id']))

			list_of_project_models = [pm for pm in self.getProjectModels(request) if pm.id != self.model_id]
			# print("list of models : %s" % [pm.name for pm in list_of_project_models])
			# print("selected model : %s" % str(list_of_project_models[int(request.POST['model_id'])].name))
			return self.getModelSubmodels(request, int(request.POST['model_id']))
			#
			# t_model = list_of_project_models[int(request.POST['model_id'])]
			# t_filename = join(settings.MEDIA_ROOT, str(t_model.sbml_file))
			# doc = SbmlDocument()
			# doc.readSbml(t_filename)
			# if doc.useCompPackage:
			#     return doc.listOfModelDefinitions.sbmlIds()+doc.listOfExternalModelDefinitions.sbmlIds()
			# else:
			#     return []
