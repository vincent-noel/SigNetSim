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

""" GetReaction.py

	This file...

"""

from libsignetsim import KineticLaw

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class GetReaction(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)


	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		reaction = self.getModel().listOfReactions.getBySbmlId(str(request.POST['sbml_id']))

		list_of_parameters = []
		for parameter in self.getModel().listOfParameters.values():
			list_of_parameters.append(parameter)

		for parameter in reaction.listOfLocalParameters.values():
			list_of_parameters.append(parameter)

		t_reaction_type = reaction.getReactionType()
		t_reaction_parameters = reaction.getReactionParameters()

		t_reaction_parameters_index = []
		if t_reaction_parameters is not None and None not in t_reaction_parameters:
			for t_param in t_reaction_parameters:
				t_reaction_parameters_index.append(list_of_parameters.index(t_param))
		else:
			t_reaction_type = KineticLaw.UNDEFINED

		self.data.update({
			'id': self.getModel().listOfReactions.values().index(reaction),
			'name': "" if reaction.getName() is None else reaction.getName(),
			'sbml_id': reaction.getSbmlId(),
			'list_of_reactants': [
				(
					self.getModel().listOfSpecies.index(reactant.getSpecies()),
					reactant.stoichiometry.getPrettyPrintMathFormula()
				)
				for reactant in reaction.listOfReactants.values()
			],
			'list_of_modifiers': [
				(
					self.getModel().listOfSpecies.index(modifier.getSpecies()),
					modifier.stoichiometry.getPrettyPrintMathFormula()
				)
				for modifier in reaction.listOfModifiers.values()
			],
			'list_of_products': [
				(
					self.getModel().listOfSpecies.index(product.getSpecies()),
					product.stoichiometry.getPrettyPrintMathFormula()
				)
				for product in reaction.listOfProducts.values()
			],
			'kinetic_law': reaction.kineticLaw.getPrettyPrintMathFormula(),
			'reaction_type': t_reaction_type,
			'reaction_type_name': KineticLaw.reactionTypes[t_reaction_type],
			'reversible': 1 if reaction.reversible else 0,
			'list_of_parameters': [] if t_reaction_parameters is None else t_reaction_parameters_index
			,
			'list_of_local_parameters': [
				[param.getNameOrSbmlId(), "" if param.getValue() is None else param.getValue()] for param in reaction.listOfLocalParameters.values()
			]
			,
			'notes': "" if reaction.getNotes() is None else reaction.getNotes(),

		})
		if reaction.getAnnotation().getSBOTerm() is not None:
			self.data.update({
				'sboterm': reaction.getAnnotation().getSBOTerm(),
				'sboterm_name': reaction.getAnnotation().getSBOTermDescription()
			})

		return JsonRequest.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)


