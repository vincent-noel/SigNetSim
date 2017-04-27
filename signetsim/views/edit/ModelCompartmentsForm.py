#!/usr/bin/env python
""" ModelCompartmentsForm.py


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
from ModelParentForm import ModelParentForm

from libsignetsim.model.ModelException import ModelException


class ModelCompartmentsForm(ModelParentForm):


	def __init__(self, parent):

		ModelParentForm.__init__(self, parent)

		self.sbmlId = None
		self.name = None
		self.size = 1
		self.unit = None
		self.constant = True

	def clear(self):

		ModelParentForm.clear(self)

	# def load(self, compartment_id):
	#
	# 	self.id = compartment_id
	#
	# 	t_compartment = self.parent.listOfCompartments[self.id]
	#
	# 	self.name = t_compartment.getName()
	# 	self.sbmlId = t_compartment.getSbmlId()
	# 	self.size = t_compartment.getSize()
	#
	# 	if t_compartment.getUnits() is not None:
	# 		self.unit = self.parent.listOfUnits.index(t_compartment.getUnits())
	#
	# 	self.constant = t_compartment.constant
	# 	self.isEditing = True


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

		except ModelException as e:
			self.addError(e.message)


	def read(self, request):

		self.id = self.readInt(request, 'compartment_id',
								"The indice of the compartment",
								required=False)

		self.name = self.readString(request, 'compartment_name',
								"The name of the compartment", required=False)

		self.sbmlId = self.readString(request, 'compartment_sbml_id',
								"The identifier of the compartment")

		self.size = self.readFloat(request, 'compartment_size',
								"The size of the compartment")

		self.unit = self.readInt(request, 'compartment_unit',
								"The indice of the unit of the compartment",
								max_value=len(self.parent.listOfUnits),
								required=False)

		self.constant = self.readOnOff(request, 'compartment_constant',
								"The constant property of the compartment")

