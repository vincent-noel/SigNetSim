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

""" ProfileView.py

	This file ...

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
			if request.POST['action'] == "change_first_name":
				self.changeFirstname(request)

			elif request.POST['action'] == "change_last_name":
				self.changeLastname(request)

			elif request.POST['action'] == "change_email":
				self.changeEmail(request)

			elif request.POST['action'] == "change_organization":
				self.changeOrganization(request)

			elif request.POST['action'] == "change_password":
				self.changePassword(request)

		return TemplateView.get(self, request, *args, **kwargs)

	def changeFirstname(self, request):
		t_firstname = self.readUnicodeString(request, 'first_name', "the first name")
		if t_firstname is not None:
			request.user.first_name = t_firstname
			request.user.save()

	def changeLastname(self, request):
		t_lastname = self.readUnicodeString(request, 'last_name', "the last name")
		if t_lastname is not None:
			request.user.last_name = t_lastname
			request.user.save()

	def changeOrganization(self, request):
		t_organization = self.readUnicodeString(request, 'organization', "the organization")
		if t_organization is not None:
			request.user.organization = t_organization
			request.user.save()

	def changeEmail(self, request):

		t_email = self.readASCIIString(request, 'email', 'The email address')
		if t_email is not None:
			try:
				validate_email(t_email)
				request.user.email = request.POST['email']
				request.user.save()
			except ValidationError:
				self.addError("Invalid email address")

	def changePassword(self, request):
		if request.POST['password1'] == request.POST['password2']:
			t_password = self.readASCIIString(request, 'password1', "the password")
			if t_password is not None:
				request.user.set_password(t_password)
				request.user.save()
