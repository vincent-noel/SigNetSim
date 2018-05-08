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

""" ModelOverviewView.py

	This file ...

"""

from django.views.generic import TemplateView
from django.shortcuts import redirect
from signetsim.views.HasWorkingModel import HasWorkingModel

class ModelOverviewView(TemplateView, HasWorkingModel):

	template_name = 'edit/overview.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)

		self.listOfSpecies = None
		self.listOfReactions = None
		self.listOfCompartments = None

	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs['list_of_species'] = self.listOfSpecies
		kwargs['list_of_reactions'] = self.listOfReactions
		kwargs['list_of_compartments'] = self.listOfCompartments
		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		if len(args) > 0:
			self.setModel(request, int(args[0]))
			return redirect('edit_overview')

		return TemplateView.get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingModel.isChooseModel(self, request):
				self.load(request, *args, **kwargs)

		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)
		self.listOfCompartments = self.getModel().listOfCompartments
		self.listOfReactions = self.getModel().listOfReactions

		if self.isModelLoaded():
			if self.isCompModelDefinition():
				self.listOfSpecies = [species for species in self.getModel().listOfSpecies]

			elif self.isCompInternalSubmodel():
				self.listOfSpecies = [species for species in self.getModel().listOfSpecies]

			elif self.isFlattenModel():
				# Would be nice to also draw the boundaries of the submodels here
				self.listOfSpecies = [species for species in self.getModel().listOfSpecies if species.isInReactions(including_modifiers=True)]

			else:

				self.listOfSpecies = [species for species in self.getModel().listOfSpecies if species.isInReactions(including_modifiers=True)]
