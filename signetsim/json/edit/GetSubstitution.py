#!/usr/bin/env python
""" GetSpecies.py


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

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel
from libsignetsim.model.Variable import Variable
from libsignetsim.model.sbml.ReplacedElement import ReplacedElement
from libsignetsim.model.sbml.ReplacedBy import ReplacedBy


class GetSubstitution(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)
		self.listOfObjects = []
		self.listOfSubmodels = []

	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		substitution_id = int(request.POST['id'])
		listOfSubstitutions = self.getModel().listOfSbmlObjects.getListOfSubstitutions()


		if substitution_id < len(listOfSubstitutions):

			substitution = listOfSubstitutions[substitution_id]

			self.data.update({
				'id': substitution_id,
			})

			if isinstance(substitution, ReplacedElement):
				self.data.update({
					'type': 0,
					'object_id': self.listOfObjects.index(substitution.getParentObject()),
					'object_name': substitution.getParentObject().getName(),
				})

				submodel = self.getModel().listOfSubmodels.getBySbmlIdRef(substitution.getSubmodelRef())
				submodel_objects = []
				for t_object in submodel.getModelObject().listOfSbmlObjects.values():
					if isinstance(t_object, Variable) and not t_object.isStoichiometry():
						submodel_objects.append(t_object)

				self.data.update({
					'submodel_id': self.listOfSubmodels.index(submodel),
					'submodel_name': submodel.getName(),
					'submodel_object_id': submodel_objects.index(substitution.getReplacedElementObject()),
					'submodel_object_name': substitution.getReplacedElementObject().getNameOrSbmlId(),
				})

			elif isinstance(substitution, ReplacedBy):
				self.data.update({
					'type': 1,
					'object_id': self.listOfObjects.index(substitution.getParentObject()),
					'object_name': substitution.getParentObject().getName(),
				})

				submodel = self.getModel().listOfSubmodels.getBySbmlIdRef(substitution.getSubmodelRef())
				submodel_objects = []
				for t_object in submodel.getModelObject().listOfSbmlObjects.values():
					if isinstance(t_object, Variable) and not t_object.isStoichiometry():
						submodel_objects.append(t_object)

				self.data.update({
					'submodel_id': self.listOfSubmodels.index(submodel),
					'submodel_name': submodel.getName(),
					'submodel_object_id': submodel_objects.index(substitution.getReplacingElement()),
					'submodel_object_name': substitution.getReplacingElement().getNameOrSbmlId(),

				})
		return JsonRequest.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)

		self.listOfObjects = []
		for object in self.getModel().listOfSbmlObjects.values():
			if isinstance(object, Variable) and not object.isStoichiometry():
				self.listOfObjects.append(object)
		self.listOfSubmodels = self.getModel().listOfSubmodels.values()
