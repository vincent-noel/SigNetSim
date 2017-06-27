#!/usr/bin/env python
""" MathValidator.py


	This file...



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

from libsignetsim.model.ModelException import ModelException
from libsignetsim.model.math.MathFormula import MathFormula

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class MathValidator(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)

	def get(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)
		self.data.update({self.model.getSbmlId(): self.model.getName()})
		return JsonRequest.get(self, request, *args, **kwargs)

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
