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
from libsignetsim.model.sbml.KineticLaw import KineticLaw
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
		self.listOfLocalParameters = None
		self.KineticLaw = None
		self.editKineticLawErrors = None
		self.SBOTerm = None

	def save(self, reaction):


		try:
			reaction.setName(self.name)
			reaction.setSbmlId(self.sbmlId)

			self.saveReactants(reaction)
			self.saveModifiers(reaction)
			self.saveProducts(reaction)

			if self.reactionType == KineticLaw.UNDEFINED:
				reaction.setKineticLaw(self.reactionType, self.reversible, math=self.kineticLaw)
			else:
				t_parameters = [self.parent.listOfParameters[param] for param in self.listOfParameters]
				reaction.setKineticLaw(self.reactionType, self.reversible, parameters=t_parameters)

			self.isEditing = False
			if self.listOfLocalParameters != []:

				reaction.listOfLocalParameters.clear()
				for (param_name, param_value) in self.listOfLocalParameters:
					t_parameter = Parameter(self.parent.getModel())
					t_parameter.new(param_name, param_value)
					reaction.listOfLocalParameters.add(t_parameter)

			if self.SBOTerm is not None:
				reaction.getAnnotation().setSBOTerm(self.SBOTerm)
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
		self.readLocalParameters(request)

		self.reactionType = self.readInt(request, 'reaction_type',
								"the type of the kinetic law",
								max_value=len(self.parent.reactionTypes))

		if self.reactionType != KineticLaw.UNDEFINED:
			self.readParameters(request)
		else:

			self.kineticLaw = self.readString(request, 'reaction_kinetic_law',
								"the formula of the reaction's kinetic law")

		self.reversible = self.readOnOff(request, 'reaction_reversible',
									"the reversible status of the reaction")

		self.SBOTerm = self.readInt(request, 'reaction_sboterm',
									"The SBO term of the reaction",
									required=False)


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

	def readLocalParameters(self, request):

		parameter_id = 0
		self.listOfLocalParameters = []

		while self.existField(request, "local_parameter_%d_name" % parameter_id):
			t_parameter_name = self.readString(
				request,
				'local_parameter_%d_name' % parameter_id,
				"the name of the local parameter #%d" % parameter_id
			)
			t_parameter_value = self.readFloat(
				request,
				'local_parameter_%d_value' % parameter_id,
				"the value of the local parameter #%d" % parameter_id,
				required=False
			)

			self.listOfLocalParameters.append((t_parameter_name, t_parameter_value))
			parameter_id += 1


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
