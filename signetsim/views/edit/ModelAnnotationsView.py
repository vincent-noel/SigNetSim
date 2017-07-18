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

from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.views.HasErrorMessages import HasErrorMessages
from signetsim.views.edit.ModelAnnotationsForm import ModelAnnotationsForm

class ModelAnnotationsView(TemplateView, HasWorkingModel, HasErrorMessages):

	template_name = 'edit/annotations.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasErrorMessages.__init__(self)
		HasWorkingModel.__init__(self)

		self.modelHistory = None
		self.modelPublication = None
		self.form = ModelAnnotationsForm(self)


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)

		kwargs['page_address'] = reverse('edit_annotations')

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
			self.form.load()
			self.modelHistory = self.getModel().modelHistory
			if len(self.getModel().getAnnotation().getIsDescribedBy()) > 0:
				self.modelPublication = self.getModel().getAnnotation().getIsDescribedBy()[0]

	def saveNotes(self, request):
		self.form.readNotes(request)
		self.form.saveNotes()
		self.saveModel(request)


	def saveName(self, request):
		self.form.readName(request)
		self.form.saveName()
		self.saveModel(request)
		self.saveModelName(self.form.name)

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
