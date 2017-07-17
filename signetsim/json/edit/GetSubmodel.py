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

from django.conf import settings
from libsignetsim.model.Model import Model
from libsignetsim.model.ModelException import ModelException
from libsignetsim.model.SbmlDocument import SbmlDocument
from os.path import join, basename

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

			submodel = self.getModel().listOfSubmodels.values()[submodel_id]

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


			self.data.update({
				'time_conversion_factor': (
					self.getModel().listOfParameters.values().index(submodel.getTimeConversionFactor())
					if submodel.getTimeConversionFactor() is not None
					else ""
				),
				'time_conversion_factor_name': (
					submodel.getTimeConversionFactor().getNameOrSbmlId()
					if submodel.getTimeConversionFactor() is not None
					else ""
				),
				'extent_conversion_factor': (
					self.getModel().listOfParameters.values().index(submodel.getExtentConversionFactor())
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


