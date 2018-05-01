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

""" ModelCompartmentsForm.py

	This file ...

"""

from .ModelParentForm import ModelParentForm
from libsignetsim import ModelException


class ModelCompartmentsForm(ModelParentForm):

	def __init__(self, parent):

		ModelParentForm.__init__(self, parent)

		self.sbmlId = None
		self.name = None
		self.size = 1
		self.unit = None
		self.constant = True
		self.SBOTerm = None

	def save(self, compartment):

		try:
			compartment.setSbmlId(self.sbmlId)
			compartment.setName(self.name)
			compartment.setSize(self.size)

			if self.unit is not None:
				compartment.setUnits(self.parent.listOfUnits[self.unit])
			else:
				compartment.setUnits(None)

			compartment.constant = self.constant
			compartment.getAnnotation().setSBOTerm(self.SBOTerm)

		except ModelException as e:
			self.addError(e.message)

	def read(self, request):

		self.id = self.readInt(
			request, 'compartment_id',
			"The indice of the compartment",
			required=False
		)

		self.name = self.readString(
			request, 'compartment_name',
			"The name of the compartment",
			required=False
		)

		self.sbmlId = self.readString(
			request, 'compartment_sbml_id',
			"The identifier of the compartment"
		)

		self.size = self.readFloat(
			request, 'compartment_size',
			"The size of the compartment"
		)

		self.unit = self.readInt(
			request, 'compartment_unit',
			"The indice of the unit of the compartment",
			max_value=len(self.parent.listOfUnits),
			required=False
		)

		self.constant = self.readOnOff(
			request, 'compartment_constant',
			"The constant property of the compartment"
		)

		self.SBOTerm = self.readInt(
			request, 'compartment_sboterm',
			"The SBO term of the compartment",
			required=False
		)
