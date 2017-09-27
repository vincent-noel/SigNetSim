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

""" GetContinuationFigure.py

	This file...

"""

from signetsim.json import JsonRequest
from signetsim.models import SbmlModel, ContinuationComputation
from signetsim.views.HasWorkingModel import HasWorkingModel


class GetContinuationFigure(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)
		self.listOfComputations = None


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		t_str = request.POST['continuation_id']

		if t_str != "":
			t_id = int(t_str)
			t_computation = self.listOfComputations[t_id]
			self.data.update({'status': str(t_computation.figure)})

		return JsonRequest.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)
		t_model = SbmlModel.objects.get(project=self.project_id, id=self.model_id)
		self.listOfComputations = ContinuationComputation.objects.filter(project=self.project, model=t_model)
