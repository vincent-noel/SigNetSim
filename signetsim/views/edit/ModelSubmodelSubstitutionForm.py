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

""" ModelSubmodelSubstitutionForm.py

	This file ...

"""

from libsignetsim import ModelException
from libsignetsim.model.Variable import Variable
from .ModelParentForm import ModelParentForm

class ModelSubmodelSubstitutionForm(ModelParentForm):

	def __init__(self, parent):

		ModelParentForm.__init__(self, parent)

		self.types = [
			'Replace a variable from a submodel with a variable from the main model (Replacement)',
			'Replace a variable from the main model with a variable from a sbmodel (Replaced by)'
		]

		self.type = None
		self.modelObject = None
		self.submodel = None
		self.submodelObject = None
		self.listOfObjects = []

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

		t_submodel = self.parent.listOfSubmodels[self.submodel].getModelObject()
		self.listOfObjects = []
		for t_object in t_submodel.listOfSbmlObjects:
			if isinstance(t_object, Variable) and not t_object.isStoichiometry():
				self.listOfObjects.append(t_object)
