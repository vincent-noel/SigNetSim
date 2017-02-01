#!/usr/bin/env python
""" ProfileView.py


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
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class ProfileView(TemplateView, HasErrorMessages):
	template_name = 'accounts/profile.html'


	def __init__(self, **kwargs):
		TemplateView.__init__(self, **kwargs)
		HasErrorMessages.__init__(self)

	def get_context_data(self, **kwargs):
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)
		return kwargs

	def get(self, request, *args, **kwargs):
		return TemplateView.get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):

		if "action" in request.POST:
			if request.POST['action'] == "change_fullname":
				self.changeFullname(request)

			elif request.POST['action'] == "change_email":
				self.changeEmail(request)

			elif request.POST['action'] == "change_password":
				self.changePassword(request)

		return TemplateView.get(self, request, *args, **kwargs)

	def changeFullname(self, request):
		t_fullname = self.readUnicodeString(request, 'fullname', "the full name")
		if t_fullname is not None:
			request.user.fullname = t_fullname
			request.user.save()

	def changeEmail(self, request):

		t_email = self.readString(request, 'email', 'The email address')
		if t_email is not None:
			try:
				validate_email(t_email)
				request.user.email = request.POST['email']
				request.user.save()
			except ValidationError:
				self.addError("Invalid email address")

	def changePassword(self, request):
		if request.POST['password1'] == request.POST['password2']:
			t_password = self.readString(request, 'password1', "the password")
			if t_password is not None:
				request.user.set_password(t_password)
				request.user.save()
