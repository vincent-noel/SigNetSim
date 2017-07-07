#!/usr/bin/env python
""" ModelOverviewView.py


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
from django.shortcuts import redirect
from signetsim.views.HasWorkingModel import HasWorkingModel

class ModelOverviewView_v2(TemplateView, HasWorkingModel):

	template_name = 'edit/overview0.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)

		self.listOfSpecies = None
		self.listOfReactions = None
		# self.interactionMatrix = None

	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs['list_of_species'] = [species for species in self.listOfSpecies if species.isInReactions()]
		kwargs['list_of_reactions'] = self.listOfReactions
		# kwargs['interaction_matrix'] = self.interactionMatrix
		# kwargs['png_graph'] = self.getSimpleGraph()
		return kwargs


	def get(self, request, *args, **kwargs):


		self.load(request, *args, **kwargs)
		if len(args) > 0:
			self.setModel(request, int(args[0]))
			return redirect('edit_overview')


		# self.updateSimpleGraph()
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingModel.isChooseModel(self, request):
				self.load(request, *args, **kwargs)

		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)
		if self.isModelLoaded():
			self.listOfSpecies = self.getModel().listOfSpecies.values()
			self.listOfReactions = self.getModel().listOfReactions.values()
			# self.model.build()
			# self.interactionMatrix = self.model.interactionMatrix
			# print self.model.jacobianMatrix
