#!/usr/bin/env python
""" ModelReactionsView.py


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
from libsignetsim.model.sbml.KineticLaw import KineticLaw
from libsignetsim.model.ModelException import ModelException
from ModelReactionsForm import ModelReactionsForm

class ModelReactionsView(TemplateView, HasWorkingModel, HasErrorMessages):

	template_name = 'edit/reactions.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasErrorMessages.__init__(self)
		HasWorkingModel.__init__(self)

		self.listOfReactions = None
		self.listOfSpecies = None
		self.listOfParameters = None
		self.listOfKineticLaws = None
		self.reactionTypes = KineticLaw.reactionTypes
		self.parametersList = KineticLaw.parametersList
		self.allowReversibleList = KineticLaw.allowReversibleList

		self.form = ModelReactionsForm(self)

	def get_context_data(self, **kwargs):

		kwargs = HasErrorMessages.get_context_data(self, **kwargs)
		kwargs = HasWorkingModel.get_context_data(self, **kwargs)

		kwargs['list_of_reactions'] = self.listOfReactions
		kwargs['list_of_kinetic_laws'] = self.listOfKineticLaws
		kwargs['list_of_species'] = [species.getNameOrSbmlId() for species in self.listOfSpecies]
		kwargs['list_of_parameters'] = [parameter.getNameOrSbmlId() for parameter in self.listOfParameters]
		kwargs['reaction_types'] = self.reactionTypes
		kwargs['parameters_list'] = self.parametersList
		kwargs['allow_reversible'] = self.allowReversibleList

		kwargs['form'] = self.form

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
				self.deleteReaction(request)

			elif request.POST['action'] == "save":
				self.saveReaction(request)

			elif request.POST['action'] == "edit_kineticlaw":
				self.form.editKineticLaw(request)

		self.load(request, *args, **kwargs)
		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasErrorMessages.clearErrors(self)
		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.loadReactions()
			self.loadSpecies()
			self.loadParameters()
			self.loadKineticLaws()


	def deleteReaction(self, request):

		t_id = self.readInt(request, 'reaction_id',
							"the identifier of the reaction",
							max_value=len(self.listOfReactions),
							reportField=False)

		try:
			self.getModel().listOfReactions.remove(self.listOfReactions[t_id])
			self.saveModel(request)
			self.loadReactions()

		except ModelException as e:
			self.addError(e.message)


	def saveReaction(self, request):

		self.form.read(request)
		if not self.form.hasErrors():

			if self.form.isNew():
				self.form.save(self.getModel().listOfReactions.new())

			else:
				if self.form.id < len(self.getModel().listOfReactions):
					self.form.save(self.listOfReactions[self.form.id])

			self.saveModel(request)
			self.loadReactions()

	def loadReactions(self):
		self.listOfReactions = self.getModel().listOfReactions.values()

	def loadKineticLaws(self):
		self.listOfKineticLaws = ["" for reaction in self.listOfReactions]

	def loadSpecies(self):
		self.listOfSpecies = self.getModel().listOfSpecies.values()

	def loadParameters(self):
		self.listOfParameters = self.getModel().listOfParameters.values()
