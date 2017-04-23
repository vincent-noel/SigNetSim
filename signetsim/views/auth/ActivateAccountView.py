#!/usr/bin/env python
""" ActivateAccountView.py


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
from signetsim.views.HasUserLoggedIn import HasUserLoggedIn
from signetsim.models import User
from django.core.mail import send_mail
from django.conf import settings

class ActivateAccountView(TemplateView, HasUserLoggedIn):

	template_name = 'accounts/activate_account.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasUserLoggedIn.__init__(self, **kwargs)
		self.activated = False

	def get_context_data(self, **kwargs):
		kwargs['activated'] = self.activated
		return kwargs


	def get(self, request, *args, **kwargs):

		if (request.user.is_staff is True
			and request.GET.get('username') != None
			and User.objects.filter(username=request.GET['username']).exists()):

			t_user = User.objects.get(username=request.GET['username'])
			t_user.is_active = True
			t_user.save()
			self.activated = True

		return TemplateView.get(self, request, *args, **kwargs)
