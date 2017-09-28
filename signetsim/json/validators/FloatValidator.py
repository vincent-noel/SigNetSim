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

""" FloatValidator.py

	This file...

"""

from signetsim.json import JsonRequest

class FloatValidator(JsonRequest):

	def __init__(self):
		JsonRequest.__init__(self)

	def post(self, request, *args, **kwargs):
		field = str(request.POST['value'])
		self.data.update({'error': self.readFloat(field)})
		return JsonRequest.post(self, request, *args, **kwargs)

	def readFloat(self, field):

		if field == "":
			return "is empty !"

		else:
			try:
				t_float = float(field)
				return ""
			except ValueError:
				return "isn't a float !"
