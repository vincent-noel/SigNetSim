#!/usr/bin/env python
""" ModelMiscView.py


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
from django.core.urlresolvers import reverse

from libsignetsim.uris.URI import URI
from libsignetsim.settings.Settings import Settings

from signetsim.models import SbmlModel
from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.views.HasErrorMessages import HasErrorMessages
from signetsim.views.edit.ModelAnnotationsForm import ModelAnnotationsForm

class ModelAnnotationsView(TemplateView, HasWorkingModel, HasErrorMessages):

	template_name = 'edit/annotations.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasErrorMessages.__init__(self)
		HasWorkingModel.__init__(self)

		# self.listOfUnits = None
		# self.listOfParameters = None
		# self.sbmlLevels = None
		self.modelHistory = None
		self.modelPublication = None
		self.form = ModelAnnotationsForm(self)


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)

		kwargs['page_address'] = reverse('edit_annotations')

		# kwargs['list_of_units'] = [unit.getName() for unit in self.listOfUnits]
		# kwargs['list_of_parameters'] = [parameter.getNameOrSbmlId() for parameter in self.listOfParameters]
		# kwargs['sbml_levels'] = self.sbmlLevels
		kwargs['model_history'] = self.modelHistory
		kwargs['model_publication'] = self.modelPublication
		kwargs['form'] = self.form




		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingModel.isChooseModel(self, request):
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "edit_model_name":
				self.saveName(request)

			elif request.POST['action'] == "edit_model_notes":
				self.saveNotes(request)


			# elif request.POST['action'] == "choose_time_unit":
			# 	self.saveTimeUnit(request)
			#
			# elif request.POST['action'] == "reset_time_unit":
			# 	self.resetTimeUnit(request)
			#
			#
			# elif request.POST['action'] == "choose_substance_unit":
			# 	self.saveSubstanceUnit(request)
			#
			# elif request.POST['action'] == "reset_substance_unit":
			# 	self.resetSubstanceUnit(request)
			#
			#
			# elif request.POST['action'] == "choose_extent_unit":
			# 	self.saveExtentUnit(request)
			#
			# elif request.POST['action'] == "reset_extent_unit":
			# 	self.resetExtentUnit(request)
			#
			#
			# elif request.POST['action'] == "choose_scaling_factor":
			# 	self.saveScalingFactor(request)
			#
			# elif request.POST['action'] == "reset_scaling_factor":
			# 	self.resetScalingFactor(request)
			#
			#
			# elif request.POST['action'] == "choose_sbml_level":
			# 	self.saveSbmlLevel(request)

			elif request.POST['action'] == "set_model_publication":
				self.setModelPublication(request)

		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasErrorMessages.clearErrors(self)
		HasWorkingModel.load(self, request, *args, **kwargs)

		if len(args) > 0:
			self.setModel(request, int(args[0]))

		if self.isModelLoaded():
			# self.listOfUnits = self.getModel().listOfUnitDefinitions.values()
			# self.listOfParameters = self.getModel().listOfParameters.values()
			# self.sbmlLevels = self.getModel().getSbmlLevels()
			self.form.load()
			self.modelHistory = self.getModel().modelHistory
			if len(self.getModel().getAnnotation().getIsDescribedBy()) > 0:
				self.modelPublication = self.getModel().getAnnotation().getIsDescribedBy()[0]

	# def saveTimeUnit(self, request):
	# 	self.form.readTimeUnit(request)
	# 	self.form.saveTimeUnit()
	# 	self.saveModel(request)
	# 
	# def resetTimeUnit(self, request):
	# 	self.form.clearTimeUnits()
	# 	self.form.saveTimeUnit()
	# 	self.saveModel(request)
	# 
	# 
	# def saveSubstanceUnit(self, request):
	# 	self.form.readSubstanceUnit(request)
	# 	self.form.saveSubstanceUnit()
	# 	self.saveModel(request)
	# 
	# def resetSubstanceUnit(self, request):
	# 	self.form.clearSubstanceUnits()
	# 	self.form.saveSubstanceUnit()
	# 	self.saveModel(request)
	# 
	# 
	# def saveExtentUnit(self, request):
	# 	self.form.readExtentUnit(request)
	# 	self.form.saveExtentUnit()
	# 	self.saveModel(request)
	# 
	# def resetExtentUnit(self, request):
	# 	self.form.clearExtentUnit()
	# 	self.form.saveExtentUnit()
	# 	self.saveModel(request)
	# 
	# 
	# def saveScalingFactor(self, request):
	# 	self.form.readScalingFactor(request)
	# 	self.form.saveScalingFactor()
	# 	self.saveModel(request)
	# 
	# def resetScalingFactor(self, request):
	# 	self.form.clearScalingFactor()
	# 	self.form.saveScalingFactor()
	# 	self.saveModel(request)


	def saveNotes(self, request):
		self.form.readNotes(request)
		self.form.saveNotes()
		self.saveModel(request)


	def saveName(self, request):
		self.form.readName(request)
		self.form.saveName()
		self.saveModel(request)
		self.saveModelName(self.form.name)


	# def saveSbmlLevel(self, request):
	# 	self.form.readSbmlLevel(request)
	# 	self.form.saveSbmlLevel()
	# 	self.saveModel(request)

	def setModelPublication(self, request):

		if str(request.POST['model_publication_pubmed_id']) != "":
			t_uri = URI()
			t_uri.setPubmed(request.POST['model_publication_pubmed_id'])
			self.getModel().getAnnotation().addIsDesribedBy(t_uri)
		else:
			self.getModel().getAnnotation().clearIsDescribedBy()

		self.saveModel(request)
		if len(self.getModel().getAnnotation().getIsDescribedBy()) > 0:
			self.modelPublication = self.getModel().getAnnotation().getIsDescribedBy()[0]
		else:
			self.modelPublication = None
