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

""" ModelSpeciesForm.py

	This file ...

"""

from libsignetsim.model.ModelException import ModelException
from ModelParentForm import ModelParentForm

class ModelSpeciesForm(ModelParentForm):

	def __init__(self, parent):

		ModelParentForm.__init__(self, parent)

		self.name = None
		self.sbmlId = None
		self.value = None
		self.constant = None
		self.boundaryCondition = False
		self.compartment = None
		self.unit = None
		self.notes = None
		self.isConcentration = None
		self.SBOTerm = None


	def save(self, species):

		try:
			if self.compartment is not None:
				species.setCompartment(self.parent.listOfCompartments[self.compartment])
			else:
				species.setCompartment(None)
			species.setName(self.name)
			species.setSbmlId(self.sbmlId)
			species.setValue(self.value)
			species.constant = self.constant
			species.hasOnlySubstanceUnits = not self.isConcentration
			species.boundaryCondition = self.boundaryCondition
			if self.unit is not None:
				species.setUnits(self.parent.listOfUnits[self.unit])
			else:
				species.setUnits(None)

			species.setNotes(self.notes)
			if self.SBOTerm is not None:
				species.getAnnotation().setSBOTerm(self.SBOTerm)

		except ModelException as e:
			self.addError(e.message)


	def read(self, request):

		self.id = self.readInt(request, 'species_id',
								"The indice of the species",
								required=False)

		self.name = self.readString(request, 'species_name',
								"The name of the species", required=False)

		self.sbmlId = self.readString(request, 'species_sbml_id',
								"The identifier of the species")

		self.value = self.readFloat(request, 'species_value',
								"The value of the species", required=False)

		self.isConcentration = self.readTrueFalse(request, 'species_value_type',
												  "the type of species")

		self.compartment = self.readInt(request, 'species_compartment',
								"The indice of the compartment of the species",
								max_value=len(self.parent.listOfCompartments))

		self.unit = self.readInt(request, 'species_unit',
								"The indice of the unit of the species",
								max_value=len(self.parent.listOfUnits),
								required=False)

		self.constant = self.readOnOff(request, 'species_constant',
								"The constant property of the species")

		self.boundaryCondition = self.readOnOff(request, 'species_boundary',
								"The boundary condition property of the species")

		self.SBOTerm = self.readInt(request, 'species_sboterm',
								"The SBO term of the species",
								 required=False)