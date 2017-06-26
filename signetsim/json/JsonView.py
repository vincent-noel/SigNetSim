#!/usr/bin/env python
""" JsonView.py


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

from django.http import JsonResponse
from django.views.generic import View

class JsonView(View):

	def __init__(self):
		View.__init__(self)
		self.data = {}

	def get(self, request, *args, **kwargs):
		return JsonResponse(self.data)

	def post(self, request, *args, **kwargs):
		return JsonResponse(self.data)
