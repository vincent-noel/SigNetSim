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

""" ModelSubmodelsForm.py

	This file ...

"""

from libsignetsim import ModelException
from libsignetsim.model.Variable import Variable
from .ModelParentForm import ModelParentForm
import os

class ModelSubmodelsForm(ModelParentForm):

	def __init__(self, parent):

		ModelParentForm.__init__(self, parent)

		self.name = None
		self.sbmlId = None
		self.modelRef = None
		self.type = None
		self.source = None
		self.submodelRef = None

		self.timeConversionFactor = None
		self.extentConversionFactor = None

		self.listOfDeletions = None
		self.listOfObjects = None
		self.listOfObjectsMetaIds = None


	def save(self, request, submodel, definition):


		try:
			submodel.setName(self.name)
			submodel.setSbmlId(self.sbmlId)
			submodel.setModelRef(self.sbmlId+"_def")
			definition.setSbmlId(self.sbmlId+"_def")

			if self.type == 1:
				if self.source is not None:
					t_filename = os.path.basename(str(self.parent.listOfProjectModels[self.source].sbml_file))
					self.parent.loadModelSubModels(request, self.source)
					definition.setSource(t_filename)

					if self.submodelRef is not None and self.submodelRef != 0 and self.submodelRef < len(self.parent.listOfSubmodelsRefs):
						definition.setModelRef(self.parent.listOfSubmodelsRef(self.submodelRef))
			elif self.type == 0:
				definition.setName(self.name)

			if self.timeConversionFactor is not None:
				factor_id = self.parent.listOfConversionFactors[self.timeConversionFactor].getSbmlId()
				submodel.setTimeConversionFactor(factor_id)
			elif submodel.hasTimeConversionFactor():
				submodel.unsetTimeConversionFactor()

			if self.extentConversionFactor is not None:
				factor_id = self.parent.listOfConversionFactors[self.extentConversionFactor].getSbmlId()
				submodel.setExtentConversionFactor(factor_id)
			elif submodel.hasExtentConversionFactor():
				submodel.unsetExtentConversionFactor()


			submodel.listOfDeletions.clear()

			if self.listOfDeletions != None:
				for deletion in self.listOfDeletions:

					# t_object = submodel.getModelObject().listOfSbmlObjects[self.listOfObjectsMetaIds[deletion]]
					t_object = submodel.getModelObject().listOfSbmlObjects.getByMetaId(self.listOfObjectsMetaIds[deletion])
					t_deletion = submodel.listOfDeletions.new()

					# here we need to choose how to address the object
					# If it's a variable, it will be via idRef
					# otherwise it will be a meta_id_ref
					if isinstance(t_object, Variable):
						t_deletion.setIdRef(t_object.getSbmlId())
					else:
						t_deletion.setMetaIdRef(t_object.getMetaId())

		except ModelException as e:
			self.addError(e.message)




	def read(self, request):

		# print request.POST

		self.id = self.readInt(request, 'submodel_id',
								"The indice of the submodel",
								required=False)

		self.name = self.readASCIIString(request, 'submodel_name',
								"The name of the submodel")

		self.sbmlId = self.readASCIIString(request, 'submodel_sbml_id',
								"The identifier of the submodel")

		self.type = self.readInt(request, 'submodel_type',
								"The type of the submodel",
								required=True, max_value=2)

		if self.type is not None and self.type == 1:
			self.source = self.readInt(request, 'submodel_source',
								"The index of the source of the submodel",
								required=True,
								max_value=len(self.parent.listOfProjectModels))

			self.parent.loadModelSubModels(request, self.source)

			self.submodelRef = self.readInt(request, 'submodel_submodel',
								"The index of the submodel in the submodel",
								required=True,
								max_value=len(self.parent.listOfSubmodelsRefs))


		self.timeConversionFactor = self.readInt(request, 'time_conversion_factor',
								"The time conversion factor of the submodel",
								required=False, max_value=len(self.parent.listOfConversionFactors))

		self.extentConversionFactor = self.readInt(request, 'extent_conversion_factor',
								"The extent conversion factor of the submodel",
								required=False, max_value=len(self.parent.listOfConversionFactors))


	def readDeletions(self, submodel, request):

		self.listOfObjects = []
		self.listOfObjectsMetaIds = []
		for object in submodel.getModelObject().listOfSbmlObjects:
			if isinstance(object, Variable) and not object.isStoichiometry():
				self.listOfObjects.append(object.getNameOrSbmlId() + (" (%s)" % type(object).__name__))
				self.listOfObjectsMetaIds.append(object.getMetaId())


		deletion_id = 0
		self.listOfDeletions = []
		while self.existField(request, 'deletion_id_%d_' % deletion_id):
			t_deletion = self.readInt(request,
							'deletion_id_%d_' % deletion_id,
							"the identifier of the deletion #%d" % deletion_id,
							max_value=len(self.listOfObjects))


			self.listOfDeletions.append(t_deletion)
			deletion_id += 1

		# print "List of deletions : %s" % str(self.listOfDeletions)
