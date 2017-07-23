#!/usr/bin/env python
""" AdminView.py


	This file ...


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

from django.views.generic import TemplateView
from signetsim.models import User
from signetsim.views.HasErrorMessages import HasErrorMessages
from signetsim.managers.users import deleteUser

class AdminView(TemplateView, HasErrorMessages):
	template_name = 'admin/admin.html'


	def __init__(self, **kwargs):
		TemplateView.__init__(self, **kwargs)
		HasErrorMessages.__init__(self)

		self.users = None


	def get_context_data(self, **kwargs):
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)
		kwargs['users'] = self.users
		return kwargs

	def get(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)
		if "action" in request.POST:
			if request.POST['action'] == "delete":
				self.deleteUser(request)

		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):
		self.users = User.objects.all()

	def deleteUser(self, request):

		if User.objects.filter(id=int(request.POST['id'])).exists():

			user = User.objects.get(id=int(request.POST['id']))
			deleteUser(user)

