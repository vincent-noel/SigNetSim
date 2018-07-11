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

""" GetCompartment.py

	This file...

"""

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class GetCompartment(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)


	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		compartment = self.getModel().listOfCompartments.getBySbmlId(str(request.POST['sbml_id']))
		self.data.update({
			'id': self.getModel().listOfCompartments.index(compartment),
			'name': "" if compartment.getName() is None else compartment.getName(),
			'sbml_id': compartment.getSbmlId(),
			'value': compartment.getValue(),
			'constant': (1 if compartment.constant else 0),
			'unit_name': "Choose a unit" if compartment.getUnits() is None else compartment.getUnits().getName(),
			'unit_id': "" if compartment.getUnits() is None else self.getModel().listOfUnitDefinitions.index(compartment.getUnits()),
			'notes': "" if compartment.getNotes() is None else compartment.getNotes()
		})
		if compartment.getAnnotation().getSBOTerm() is not None:
			self.data.update({
				'sboterm': compartment.getAnnotation().getSBOTerm(),
				'sboterm_name': compartment.getAnnotation().getSBOTermDescription()
			})

		return JsonRequest.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)


