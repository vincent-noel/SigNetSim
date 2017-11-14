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

""" ModelUnitsForm.py

	This file ...

"""

from signetsim.views.edit.ModelParentForm import ModelParentForm
from libsignetsim.model.sbml.Unit import Unit


class ModelUnitsForm(ModelParentForm):

	template_name = 'edit/units.html'

	def __init__(self, parent):

		ModelParentForm.__init__(self, parent)

		self.name = None
		self.unitId = None
		self.listOfUnits = []

	def save(self, unit_definition):

		unit_definition.setName(str(self.name))
		unit_definition.setSbmlId(str(self.unitId))
		unit_definition.listOfUnits = []

		for (kind, exponent, scale, multiplier) in self.listOfUnits:
			t_unit = unit_definition.newUnit()
			t_unit.new(kind, exponent, scale, multiplier)


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

		while ("subunit_id_%d" % i) in request.POST:
			t_unit = self.readInt(
				request, 'subunit_id_%d' % i,
				"the kind of the unit #%d" % i,
				max_value=len(Unit.unit_id)
			)

			t_exponent = self.readInt(
				request, 'subunit_exponent_%d' % i,
				"the exponent of the unit #%d" % i
			)

			t_scale = self.readInt(
				request, 'subunit_scale_%d' % i,
				"the scale of the unit #%d" % i
			)

			t_multiplier = self.readFloat(
				request, 'subunit_multiplier_%d' % i,
				"the multiplier of the unit #%d" % i
			)

			self.listOfUnits.append((Unit.unit_id.keys()[t_unit], t_exponent, t_scale, t_multiplier))

			i += 1
