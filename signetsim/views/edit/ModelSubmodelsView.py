#!/usr/bin/env python
""" ModelSubmodelsView.py


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

from django.views.generic import TemplateView
from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.views.HasErrorMessages import HasErrorMessages
from ModelSubmodelsForm import ModelSubmodelsForm
from ModelSubmodelSubstitutionForm import ModelSubmodelSubstitutionForm
from libsignetsim.model.ModelException import ModelException
from libsignetsim.model.Variable import Variable
from libsignetsim.model.sbml.ReplacedElement import ReplacedElement
from libsignetsim.model.sbml.ReplacedBy import ReplacedBy

class ModelSubmodelsView(TemplateView, HasWorkingModel, HasErrorMessages):

	template_name = 'edit/submodels.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasErrorMessages.__init__(self)
		HasWorkingModel.__init__(self)

		self.listOfSubmodels = []
		self.listOfSubmodelTypes = []
		self.listOfSubstitutions = None

		self.listOfProjectModels = None
		self.listOfSubmodelsRefs = None
		self.listOfObjects = None
		self.listOfObjectsMetaIds = None
		self.listOfConversionFactors = None

		self.form = ModelSubmodelsForm(self)
		self.formSubstitutions = ModelSubmodelSubstitutionForm(self)


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)

		kwargs['list_of_submodels'] = self.listOfSubmodels
		kwargs['list_of_substitutions'] = self.listOfSubstitutions

		kwargs['list_of_project_models'] = [str(pm.name) for pm in self.listOfProjectModels]
		kwargs['list_of_submodels_refs'] = self.listOfSubmodelsRefs
		kwargs['list_of_submodel_types'] = self.listOfSubmodelTypes

		kwargs['list_of_objects'] = self.listOfObjects
		kwargs['list_of_conversion_factors'] = [conv_factor.getNameOrSbmlId() for conv_factor in self.listOfConversionFactors]

		kwargs['form'] = self.form
		kwargs['form_subs'] = self.formSubstitutions

		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingModel.isChooseModel(self, request):
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "delete":
				self.deleteSubmodel(request)

			elif request.POST['action'] == "save":
				self.saveSubmodel(request)

			elif request.POST['action'] == "delete_substitution":
				self.deleteSubstitution(request)

			elif request.POST['action'] == "save_substitution":
				self.saveSubstitution(request)

		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasErrorMessages.clearErrors(self)
		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.loadSubmodels()
			self.loadProjectModels(request)
			self.loadConversionFactors()
			self.loadObjects()
			self.loadSubstitutions()


	def deleteSubmodel(self, request):

		submodel_id = self.readInt(request, 'submodel_id',
									"the identifier of the submodel",
									max_value=len(self.listOfSubmodels),
									reportField=False)

		try:
			t_submodel = self.listOfSubmodels[submodel_id]
			self.model.listOfSubmodels.remove(t_submodel)

			if self.listOfSubmodelTypes[submodel_id] == 0:
				t_def = self.model.parentDoc.listOfModelDefinitions.getBySbmlId(t_submodel.getModelRef())
				self.model.parentDoc.listOfModelDefinitions.remove(t_def)
			elif self.listOfSubmodelTypes[submodel_id] == 1:
				t_def = self.model.parentDoc.listOfExternalModelDefinitions.getBySbmlId(t_submodel.getModelRef())
				self.model.parentDoc.listOfExternalModelDefinitions.remove(t_def)

			self.saveModel(request)
			self.loadSubmodels()

		except ModelException as e:
			self.addError(e.message)


	def saveSubmodel(self, request):

		self.form.read(request)
		if not self.form.hasErrors():

			if self.form.isNew():
				if self.form.type == 0:

					if not self.model.parentDoc.isCompEnabled():
						self.model.parentDoc.enableComp()

					new_submodel = self.model.listOfSubmodels.new()
					# self.form.readDeletions(new_submodel, request)
					new_definition = self.model.parentDoc.listOfModelDefinitions.new()
					self.form.save(request, new_submodel, new_definition)

				if self.form.type == 1:

					if not self.model.parentDoc.isCompEnabled():
						self.model.parentDoc.enableComp()

					new_submodel = self.model.listOfSubmodels.new()
					# self.form.readDeletions(new_submodel, request)

					new_definition = self.model.parentDoc.listOfExternalModelDefinitions.new()

					self.form.save(request, new_submodel, new_definition)

			else:

				t_submodel = self.listOfSubmodels[self.form.id]
				self.form.readDeletions(t_submodel, request)
				if self.listOfSubmodelTypes[self.form.id] == 0:
					t_def = self.model.parentDoc.listOfModelDefinitions.getBySbmlId(t_submodel.getModelRef())

				elif self.listOfSubmodelTypes[self.form.id] == 1:
					t_def = self.model.parentDoc.listOfExternalModelDefinitions.getBySbmlId(t_submodel.getModelRef())

				self.form.save(request, t_submodel, t_def)

			self.saveModel(request)
			self.loadSubmodels()
			self.form.clear()



	def deleteSubstitution(self, request):

		substitution_id = self.readInt(request, 'substitution_id',
									"the identifier of the substitution",
									max_value=len(self.listOfSubstitutions),
									reportField=False)

		try:
			t_substitution = self.listOfSubstitutions[substitution_id]
			if t_substitution[0] == 0:
				t_model_obj = t_substitution[1]
				t_model_obj.removeReplacedElement(t_substitution[3])


			if t_substitution[0] == 1:
				t_model_obj = t_substitution[1]
				t_model_obj.unsetReplacedBy()

			self.saveModel(request)
			self.loadSubstitutions()

		except ModelException as e:
			self.addError(e.message)

	def saveSubstitution(self, request):

		self.formSubstitutions.read(request)
		if not self.formSubstitutions.hasErrors():

			if self.formSubstitutions.isNew():
				if self.formSubstitutions.type == 0:
					t_metaid = self.listOfObjectsMetaIds[self.formSubstitutions.modelObject]
					t_object = self.model.listOfSbmlObjects.getByMetaId(t_metaid)
					t_replacement = t_object.addReplacedElement()
					self.formSubstitutions.save(request, t_replacement)


				if self.formSubstitutions.type == 1:
					t_metaid = self.listOfObjectsMetaIds[self.formSubstitutions.modelObject]
					t_object = self.model.listOfSbmlObjects.getByMetaId(t_metaid)
					t_replaced_by = t_object.getReplacedBy()
					self.formSubstitutions.save(request, t_replaced_by)


			else:

				if self.formSubstitutions.id < len(self.listOfSubstitutions):

					listOfSubstitutions = self.getModel().listOfSbmlObjects.getListOfSubstitutions()
					self.formSubstitutions.save(request, listOfSubstitutions[self.formSubstitutions.id])

			self.saveModel(request)
			self.loadSubstitutions()
			self.form.clear()


	def loadSubmodels(self):

		self.listOfSubmodels = []
		self.listOfSubmodelTypes = []
		if self.getModel().parentDoc.useCompPackage:
			self.listOfSubmodels = self.getModel().listOfSubmodels.values()

			for submodel in self.listOfSubmodels:
				if submodel.getModelRef() in self.model.parentDoc.listOfModelDefinitions.sbmlIds():
					self.listOfSubmodelTypes.append(0)
				if submodel.getModelRef() in self.model.parentDoc.listOfExternalModelDefinitions.sbmlIds():
					self.listOfSubmodelTypes.append(1)


	def loadProjectModels(self, request):
		self.listOfProjectModels = [pm for pm in self.getProjectModels(request) if pm.id != self.model_id]


	def loadModelSubModels(self, request, model_id):
		self.listOfSubmodelsRefs = self.getModelSubmodels(request, model_id)


	def loadConversionFactors(self):
		self.listOfConversionFactors = self.model.listOfParameters.values()

	def loadObjects(self):
		self.listOfObjects = []
		self.listOfObjectsMetaIds = []
		for object in self.model.listOfSbmlObjects.values():
			if isinstance(object, Variable) and not object.isStoichiometry():
				self.listOfObjects.append(object.getNameOrSbmlId() + (" (%s)" % type(object).__name__))
				self.listOfObjectsMetaIds.append(object.getMetaId())

	def loadSubstitutions(self):
		self.listOfSubstitutions = self.getModel().listOfSbmlObjects.getListOfSubstitutions_old()
