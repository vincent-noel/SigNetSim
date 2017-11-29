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

""" GetSpecies.py

	This file...

"""

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class GetSpecies(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)


	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		species = self.getModel().listOfSpecies.getBySbmlId(str(request.POST['sbml_id']))

		self.data.update({
			'id': self.getModel().listOfSpecies.values().index(species),
			'name': "" if species.getName() is None else species.getName(),
			'sbml_id': species.getSbmlId(),
			'compartment_name': species.getCompartment().getNameOrSbmlId(),
			'compartment_id': self.getModel().listOfCompartments.values().index(species.getCompartment()),
			'value': species.getValue(),
			'isConcentration': 1 if not species.hasOnlySubstanceUnits else 0,
			'constant': (1 if species.constant else 0),
			'boundaryCondition': (1 if species.boundaryCondition else 0),
			'notes': "" if species.getNotes() is None else species.getNotes(),
		})

		if species.getUnits() is not None:
			self.data.update({
				'unit_name': "" if species.getUnits().getName() is None else species.getUnits().getName(),
				'unit_id': self.getModel().listOfUnitDefinitions.values().index(species.getUnits()),
			})
		if species.getAnnotation().getSBOTerm() is not None:
			self.data.update({
				'sboterm': species.getAnnotation().getSBOTerm(),
				'sboterm_name': species.getAnnotation().getSBOTermDescription()
			})

		return JsonRequest.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)


