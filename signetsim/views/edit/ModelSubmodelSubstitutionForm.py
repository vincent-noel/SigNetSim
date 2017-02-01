#!/usr/bin/env python
""" ModelSubmodelSubstitutionForm.py


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

from libsignetsim.model.ModelException import ModelException
from libsignetsim.model.Variable import Variable
from signetsim.views.edit.ModelParentForm import ModelParentForm

class ModelSubmodelSubstitutionForm(ModelParentForm):

	def __init__(self, parent):

		ModelParentForm.__init__(self, parent)

		self.types = ['Replace a variable from a submodel with a variable from the main model (Replacement)', 'Replace a variable from the main model with a variable from a sbmodel (Replaced by)']

		self.type = None
		self.modelObject = None
		self.submodel = None
		self.submodelObject = None
		self.listOfObjects = []

	def load(self, request, substitution):

		self.type = substitution[0]


		self.modelObject = self.parent.listOfObjectsMetaIds.index(substitution[1].getMetaId())

		t_submodel_ids = [submodel.getSbmlId() for submodel in self.parent.listOfSubmodels]
		self.submodel = t_submodel_ids.index(substitution[2][0])
		self.loadSubmodelObjects()
		self.submodelObject = self.listOfObjects.index(substitution[3])

		self.isEditing = True


	def save(self, request, replacement):

		try:
			if self.type == 0:
				replacement.setSubmodelRef(self.parent.listOfSubmodels[self.submodel].getSbmlId())

				t_object = self.listOfObjects[self.submodelObject]
				if isinstance(t_object, Variable):
					replacement.setIdRef(t_object.getSbmlId())
				else:
					replacement.setMetaIdRef(t_object.getMetaId())

			if self.type == 1:
				replacement.setSubmodelRef(self.parent.listOfSubmodels[self.submodel].getSbmlId())

				t_object = self.listOfObjects[self.submodelObject]
				if isinstance(t_object, Variable):
					replacement.setIdRef(t_object.getSbmlId())
				else:
					replacement.setMetaIdRef(t_object.getMetaId())

		except ModelException as e:
			self.addError(e.message)


	def read(self, request):

		self.id = self.readInt(request, 'substitution_id',
								"The indice of the submodel's modification",
								required=False)

		self.type = self.readInt(request, 'substitution_type',
								"The indice of the submodel's modification",
								required=True, max_value=2)

		self.modelObject = self.readInt(request, 'substitution_model_object',
								"The indice of the model's object",
								required=True, max_value=len(self.parent.listOfObjects))

		self.submodel = self.readInt(request, 'substitution_submodel',
								"The indice of the submodel",
								required=True, max_value=len(self.parent.listOfSubmodels))

		self.loadSubmodelObjects()

		self.submodelObject = self.readInt(request, 'substitution_submodel_object',
								"The indice of the submodel's object",
								required=True, max_value=len(self.listOfObjects))


	def loadSubmodelObjects(self):

		# print self.submodel
		# print self.parent.listOfSubmodels
		# print self.parent.listOfSubmodels[self.submodel]
		# print self.parent.listOfSubmodels[self.submodel].getModelObject()
		t_submodel = self.parent.listOfSubmodels[self.submodel].getModelObject()
		self.listOfObjects = []
		for t_object in t_submodel.listOfSbmlObjects.values():
			if isinstance(t_object, Variable) and not t_object.isStoichiometry():
				self.listOfObjects.append(t_object)
				# print "POIL"

		# print [obj.getNameOrSbmlId() for obj in self.listOfObjects]
