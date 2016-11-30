#!/usr/bin/env python
""" ModelReactionsForm.py


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

from libsignetsim.model.ModelException import ModelException
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.math.MathKineticLaw import MathKineticLaw
from signetsim.views.edit.ModelParentForm import ModelParentForm

class ModelReactionsForm(ModelParentForm):


	def __init__(self, parent):

		ModelParentForm.__init__(self, parent)

		self.name = None
		self.sbmlId = None

		self.listOfReactants = None
		self.listOfModifiers = None
		self.listOfProducts = None

		self.reactionType = None
		self.reversible = 0
		self.listOfParameters = None
		self.KineticLaw = None
		self.editKineticLawErrors = None


	def clear(self):

		ModelParentForm.clear(self)

		self.name = None
		self.sbmlId = None

		self.listOfReactants = []
		self.listOfModifiers = []
		self.listOfProducts = []

		self.reactionType = None
		self.reversible = 0
		self.listOfParameters = None
		self.reactionKineticLaw = None
		self.editKineticLawErrors = None


	def load(self, reaction):

		self.id = self.parent.listOfReactions.index(reaction)
		self.sbmlId = reaction.getSbmlId()
		self.name = reaction.getName()
		self.reactionType = reaction.getReactionType()
		self.reactionTypeName = self.parent.reactionTypes[self.reactionType]
		self.reversible = reaction.reversible
		self.kineticLaw = reaction.kineticLaw.getPrettyPrintMathFormula()
		self.loadReactants(reaction)
		self.loadModifiers(reaction)
		self.loadProducts(reaction)
		if self.reactionType != MathKineticLaw.UNDEFINED:
			self.loadParameters(reaction)

		self.isEditing = True


	def save(self, reaction):


		try:
			reaction.setName(self.name)
			reaction.setSbmlId(self.sbmlId)

			self.saveReactants(reaction)
			self.saveModifiers(reaction)
			self.saveProducts(reaction)

			if self.reactionType == MathKineticLaw.UNDEFINED:
				reaction.setKineticLaw(self.reactionType, self.reversible, math=self.kineticLaw)
			else:
				t_parameters = [self.parent.listOfParameters[param] for param in self.listOfParameters]
				print "saving"
				print t_parameters
				reaction.setKineticLaw(self.reactionType, self.reversible, parameters=t_parameters)

			self.isEditing = False

		except ModelException as e:
			self.addError(e.message)


	def read(self, request):

		self.isEditing = True

		self.id = self.readInt(request, 'reaction_id',
								"the id of the reaction", required=False)

		self.name = self.readString(request, 'reaction_name',
							"the name of the reaction")

		self.sbmlId = self.readString(request, 'reaction_sbml_id',
							"the identifier of the reaction")

		self.readReactants(request)
		self.readProducts(request)
		self.readModifiers(request)

		print self.listOfReactants

		self.reactionType = self.readInt(request, 'reaction_type',
								"the type of the kinetic law",
								max_value=len(self.parent.reactionTypes))

		if self.reactionType != MathKineticLaw.UNDEFINED:
			self.readParameters(request)
			print "parameters"
			print self.listOfParameters
		else:

			self.kineticLaw = self.readString(request, 'reaction_kinetic_law',
								"the formula of the reaction's kinetic law")

		self.reversible = self.readOnOff(request, 'reaction_reversible',
									"the reversible status of the reaction")




	def loadReactants(self, reaction):

		self.listOfReactants = []
		for sr in reaction.listOfReactants.values():
			self.listOfReactants.append(
					(self.parent.listOfSpecies.index(sr.getSpecies()),
					sr.stoichiometry.getValueMathFormula()))


	def loadModifiers(self, reaction):

		self.listOfModifiers = []
		for sr in reaction.listOfModifiers.values():
			self.listOfModifiers.append(
					(self.parent.listOfSpecies.index(sr.getSpecies()),
					sr.stoichiometry.getValueMathFormula()))


	def loadProducts(self, reaction):

		self.listOfProducts = []
		for sr in reaction.listOfProducts.values():
			self.listOfProducts.append(
					(self.parent.listOfSpecies.index(sr.getSpecies()),
					sr.stoichiometry.getValueMathFormula()))


	def loadParameters(self, reaction):

		self.listOfParameters = []

		if reaction.getReactionParameters() is not None:
			for t_param in reaction.getReactionParameters():
				self.listOfParameters.append(
						self.parent.listOfParameters.index(t_param))

	def readReactants(self, request):

		reactant_id = 0
		self.listOfReactants = []
		while self.existField(request, 'reaction_reactant_%d' % reactant_id):
			t_species = self.readInt(request,
						 'reaction_reactant_%d' % reactant_id,
						 "the identifier of the reactant #%d" % reactant_id,
						 max_value=len(self.parent.listOfSpecies))

			t_stoichiometry = self.readFloat(request,
						'reaction_reactant_%d_stoichiometry' % reactant_id,
						"the stoichiometry of the reactant #%d" % reactant_id)

			self.listOfReactants.append((t_species, t_stoichiometry))
			reactant_id += 1


	def readProducts(self, request):

		product_id = 0
		self.listOfProducts = []
		while self.existField(request, 'reaction_product_%d' % product_id):
			t_species = self.readInt(request,
							'reaction_product_%d' % product_id,
							"the identifier of the product #%d" % product_id,
							max_value=len(self.parent.listOfSpecies))

			t_stoichiometry = self.readFloat(request,
							'reaction_product_%d_stoichiometry' % product_id,
							"the stoichiometry of the product #%d" % product_id)

			self.listOfProducts.append((t_species, t_stoichiometry))
			product_id += 1


	def readModifiers(self, request):

		modifier_id = 0
		self.listOfModifiers = []
		while self.existField(request, 'reaction_modifier_%d' % modifier_id):

			t_species = self.readInt(request,
							'reaction_modifier_%d' % modifier_id,
							"the identifier of the modifier #%d" % modifier_id,
							max_value=len(self.parent.listOfSpecies))

			t_stoichiometry = self.readFloat(request,
						'reaction_modifier_%d_stoichiometry' % modifier_id,
						"the stoichiometry of the modifier #%d" % modifier_id)

			self.listOfModifiers.append((t_species, t_stoichiometry))
			modifier_id += 1


	def readParameters(self, request):

		parameter_id = 0
		self.listOfParameters = []

		while self.existField(request, "reaction_parameter_%d" % parameter_id):
			# print "loop %d" % parameter_id
			t_parameter = self.readInt(request,
					'reaction_parameter_%d' % parameter_id,
					"the identifier of the parameter #%d" % parameter_id,
					max_value=len(self.parent.listOfParameters))

			self.listOfParameters.append(t_parameter)
			parameter_id += 1
			# print self.listOfParameters


	def saveReactants(self, reaction):

		reaction.listOfReactants.clear()
		for (species_id, stoichiometry) in self.listOfReactants:
			t_reactant = reaction.listOfReactants.new()
			t_reactant.setSpecies(self.parent.listOfSpecies[species_id])
			t_reactant.setStoichiometry(stoichiometry)

		print reaction.listOfReactants.keys()


	def saveModifiers(self, reaction):

		reaction.listOfModifiers.clear()
		for (species_id, stoichiometry) in self.listOfModifiers:
			t_modifier = reaction.listOfModifiers.new()
			t_modifier.setSpecies(self.parent.listOfSpecies[species_id])
			t_modifier.setStoichiometry(stoichiometry)


	def saveProducts(self, reaction):

		reaction.listOfProducts.clear()
		for (species_id, stoichiometry) in self.listOfProducts:
			t_product = reaction.listOfProducts.new()
			t_product.setSpecies(self.parent.listOfSpecies[species_id])
			t_product.setStoichiometry(stoichiometry)
