#!/usr/bin/env python
""" GetSubmodels.py


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
from libsignetsim.model.Model import Model
from libsignetsim.model.ModelException import ModelException
from libsignetsim.model.SbmlDocument import SbmlDocument
from os.path import join

from signetsim.json import JsonView
from signetsim.views.HasWorkingModel import HasWorkingModel


class GetSubmodels(JsonView, HasWorkingModel):

	def __init__(self):
		JsonView.__init__(self)
		HasWorkingModel.__init__(self)


	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		t_list = self.getSubmodelList(request)
		self.data.update({'list': t_list})

		return JsonView.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)


	def getSubmodelList(self, request):

		if str(request.POST['model_id']) != "":
			print "model id = %d" % int(request.POST['model_id'])

			list_of_project_models = [pm for pm in self.getProjectModels(request) if pm.id != self.model_id]
			print "list of models : %s" % [pm.name for pm in list_of_project_models]
			print "selected model : %s" % str(list_of_project_models[int(request.POST['model_id'])].name)
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
