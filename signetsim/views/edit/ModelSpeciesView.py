#!/usr/bin/env python
""" ModelSpeciesView.py


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
from libsignetsim.model.ModelException import ModelException
from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.views.HasErrorMessages import HasErrorMessages
from ModelSpeciesForm import ModelSpeciesForm

class ModelSpeciesView(TemplateView, HasWorkingModel, HasErrorMessages):

	template_name = 'edit/species.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasErrorMessages.__init__(self)
		HasWorkingModel.__init__(self)

		self.listOfSpecies = None
		self.listOfCompartments = None
		self.listOfUnits = None
		self.form = ModelSpeciesForm(self)


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)

		kwargs['list_of_species'] = self.listOfSpecies
		kwargs['list_of_compartments'] = [comp.getNameOrSbmlId() for comp in self.listOfCompartments]
		kwargs['list_of_units'] = [unit.getName() for unit in self.listOfUnits]

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
				self.deleteSpecies(request)

			elif request.POST['action'] == "save":
				self.saveSpecies(request)


		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasErrorMessages.clearErrors(self)
		HasWorkingModel.load(self, request, *args, **kwargs)
		if self.isModelLoaded():
			self.loadSpecies()
			self.loadCompartments()
			self.loadUnits()




	def deleteSpecies(self, request):

		species_id = self.readInt(request, 'species_id',
								  "the identifier of the species",
								  max_value=len(self.listOfSpecies))

		try:
			self.getModel().listOfSpecies.remove(self.listOfSpecies[species_id])
			self.saveModel(request)
			self.loadSpecies()

		except ModelException as e:
			self.addError(e.message)

	def saveSpecies(self, request):

		self.form.read(request)
		if not self.form.hasErrors():

			if self.form.isNew():
				t_species = self.getModel().listOfSpecies.new()
				self.form.save(t_species)

			else:
				if self.form.id < len(self.getModel().listOfSpecies):
					t_species = self.getModel().listOfSpecies[self.listOfSpecies[self.form.id].objId]
					self.form.save(t_species)

			self.saveModel(request)
			self.loadSpecies()
			self.form.clear()

	def loadSpecies(self):
		self.listOfSpecies = self.getModel().listOfSpecies.values()

	def loadCompartments(self):
		self.listOfCompartments = self.getModel().listOfCompartments.values()

	def loadUnits(self):
		self.listOfUnits = self.getModel().listOfUnitDefinitions.values()
