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

""" GetEquilibriumCurve.py

	This file...

"""

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.models import ContinuationComputation, SbmlModel

from dill import loads

class GetEquilibriumCurve(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)
		self.listOfComputations = None

	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		continuation_id = int(request.POST['id'])
		continuation = self.listOfComputations[continuation_id]

		if continuation.result is not None and continuation.result != '':
			parameter = self.getModel().listOfVariables.getBySymbolStr(str(continuation.parameter))

			if parameter.getUnits() is not None:
				parameter_unit = str(parameter.getUnits())
			else:
				parameter_unit = ""

			t_object = loads(continuation.result.encode('Latin-1'))
			x, ys, stab = t_object.getStabilitySlicedCurves()
			points = t_object.getPoints()

			self.data.update({
				'curve_x': x,
				'curve_ys': ys,
				'stability': stab,
				'points': points,
				'parameter': parameter.getNameOrSbmlId(),
				'parameter_unit': parameter_unit
			})

			if t_object.hasHopfBifurcations():
				x, ys = t_object.getLimitCycleCurves()
				self.data.update({
					'curve_lc_x': x,
					'curve_lc_ys': ys
				})


		return JsonRequest.post(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)
		t_model = SbmlModel.objects.get(project=self.project_id, id=self.model_id)
		self.listOfComputations = ContinuationComputation.objects.filter(project=self.project, model=t_model)

