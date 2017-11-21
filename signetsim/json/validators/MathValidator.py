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

""" MathValidator.py

	This file...

"""

from libsignetsim import ModelException, MathFormula

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class MathValidator(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)

	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		try:
			t_math = MathFormula(self.model)
			t_math.setPrettyPrintMathFormula(str(request.POST['math']))
			self.data.update({'valid': 'true'})

		except ModelException as e:
			self.data.update({'valid': 'false'})

		return JsonRequest.post(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)
