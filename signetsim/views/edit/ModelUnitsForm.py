#!/usr/bin/env python
""" ModelUnitsForm.py


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
from signetsim.views.edit.ModelParametersForm import ModelParametersForm
from libsignetsim.model.sbml.Unit import Unit


class ModelUnitsForm(ModelParametersForm):

	template_name = 'edit/units.html'

	def __init__(self, parent):

		ModelParametersForm.__init__(self, parent)

		self.name = None
		self.unitId = None
		self.listOfUnits = []

	def read(self, request):

		self.id = self.readInt(
			request, "unit_definition_id",
			"the indice of the unit definition",
			required=False
		)

		self.name = self.readUnicodeString(
			request, "unit_definition_name",
			"the name of the unit definition"
		)

		self.unitId = self.readUnicodeString(
			request, "unit_definition_identifier",
			"the identifier of the unit definition"
		)

		self.listOfUnits = []
		i = 0
		while ("unit_id_%d" % i) in request.POST:
			t_unit = self.readInt(
				request, 'unit_id_%d' % i,
				"the kind of the unit #%d" % i,
				max_value=len(Unit.unit_id)
			)

			t_exponent = self.readInt(
				request, 'unit_exponent_%d' % i,
				"the exponent of the unit #%d" % i
			)

			t_scale = self.readInt(
				request, 'unit_scale_%d' % i,
				"the scale of the unit #%d" % i
			)

			t_multiplier = self.readFloat(
				request, 'unit_multiplier_%d' % i,
				"the multiplier of the unit #%d" % i
			)

			self.listOfUnits.append((t_unit, t_exponent, t_scale, t_multiplier))
