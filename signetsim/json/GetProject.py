#!/usr/bin/env python
""" GetProject.py


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

from signetsim.json import JsonRequest
from signetsim.views.HasUserLoggedIn import HasUserLoggedIn
from signetsim.models import Project

class GetProject(JsonRequest, HasUserLoggedIn):

	def __init__(self):
		JsonRequest.__init__(self)
		HasUserLoggedIn.__init__(self)


	def post(self, request, *args, **kwargs):

		if self.isUserLoggedIn(request):

			if Project.objects.filter(id=int(request.POST['id'])).exists():
				project = Project.objects.get(id=int(request.POST['id']))
				self.data.update({
					'name': project.name,
					'public': 1 if project.access == "PU" else 0
				})

		return JsonRequest.post(self, request, *args, **kwargs)


