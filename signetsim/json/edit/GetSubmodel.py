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

""" GetSubmodel.py

	This file...

"""
from os.path import basename

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class GetSubmodel(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)


	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		submodel_id = int(request.POST['id'])

		if submodel_id < len(self.getModel().listOfSubmodels):

			submodel = self.getModel().listOfSubmodels[submodel_id]

			self.data.update({
				'id': submodel_id,
				'name': submodel.getName(),
				'sbml_id': submodel.getSbmlId(),
				'type': 1 if submodel.getModelRef() in self.getModel().parentDoc.listOfExternalModelDefinitions.sbmlIds() else 0
			})

			if self.data['type'] == 1:
				definition = self.getModel().parentDoc.listOfExternalModelDefinitions.getBySbmlId(submodel.getModelRef())
				sbml_files = [basename(str(pm.sbml_file)) for pm in self.getProjectModels(request) if pm.id != self.model_id]
				sbml_names = [str(pm.name) for pm in self.getProjectModels(request) if pm.id != self.model_id]

				if definition.getSource() in sbml_files:
					self.data.update({
						'source': sbml_files.index(definition.getSource()),
						'source_name': sbml_names[sbml_files.index(definition.getSource())]
					})

					if definition.hasModelRef():
						listOfSubmodelsRefs = self.getModelSubmodels(request, sbml_files.index(definition.getSource()))

						self.data.update({
							'source_submodel_ref': listOfSubmodelsRefs.index(definition.getModelRef()),
							'source_submodel_ref_name': definition.getModelRef()
						})
					else:
						self.data.update({
							'source_submodel_ref': 0,
							'source_submodel_ref_name': "Main model"
						})

				#
				# listOfObjects = []
				# for object in submodel.getModelObject().listOfSbmlObjects.values():
				# 	if isinstance(object, Variable) and not object.isStoichiometry():
				# 		listOfObjects.append(object.getNameOrSbmlId() + (" (%s)" % type(object).__name__))
				# 		self.listOfObjectsMetaIds.append(object.getMetaId())
				#
				# self.listOfDeletions = []
				# for deletion in submodel.listOfDeletions.values():
				# 	t_index = self.listOfObjectsMetaIds.index(deletion.getDeletionObject().getMetaId())
				# 	self.listOfDeletions.append(t_index)



			self.data.update({
				'time_conversion_factor': (
					self.getModel().listOfParameters.index(submodel.getTimeConversionFactor())
					if submodel.getTimeConversionFactor() is not None
					else ""
				),
				'time_conversion_factor_name': (
					submodel.getTimeConversionFactor().getNameOrSbmlId()
					if submodel.getTimeConversionFactor() is not None
					else ""
				),
				'extent_conversion_factor': (
					self.getModel().listOfParameters.index(submodel.getExtentConversionFactor())
					if submodel.getExtentConversionFactor() is not None
					else ""
				),
				'extent_conversion_factor_name': (
					submodel.getExtentConversionFactor().getNameOrSbmlId()
					if submodel.getExtentConversionFactor() is not None
					else ""
				),
			})

		return JsonRequest.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)


