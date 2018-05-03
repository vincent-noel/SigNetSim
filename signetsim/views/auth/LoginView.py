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

""" LoginView.py

	This file ...

"""

from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from signetsim.models import User
from signetsim.views.HasErrorMessages import HasErrorMessages
from django.conf import settings


class LoginForm(HasErrorMessages):

	def __init__(self, parent_view):

		HasErrorMessages.__init__(self)

		self.parent_view = parent_view
		self.username = None
		self.password = None

	def read(self, request):

		self.username = self.readASCIIString(request, 'username', 'the username')
		self.password = self.readASCIIString(request, 'password', 'the password')


class LoginView(TemplateView):

	template_name = 'accounts/login.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		self.form = LoginForm(self)


	def get_context_data(self, **kwargs):

		kwargs = HasErrorMessages.get_context_data(self.form, **kwargs)
		kwargs['form'] = self.form
		return kwargs


	def get(self, request, *args, **kwargs):
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		if "action" in request.POST:
			if request.POST['action'] == "login":
				if self.login(request) is True:
					# Always redirect to home
					# if request.POST.get('referer') is None or str(request.POST.get('referer')) == "http://127.0.0.1:8000/accounts/login/":
					return redirect('home')
					# else:
					# 	return HttpResponseRedirect(request.POST.get('referer'))

		return TemplateView.get(self, request, *args, **kwargs)


	def login(self, request):

		self.form.read(request)
		if not self.form.hasErrors():
			if User.objects.filter(username=self.form.username).exists():

				# user = User.objects.get(username=self.form.username)
				auth_user = authenticate(username=self.form.username, password=self.form.password)
				if auth_user is not None:
					if auth_user.is_active:
						login(self.request, auth_user)
						return True
					else:
						self.form.addError("The user account is not activated yet !")
				else:
					self.form.addError("The password doesn't match !")
			else:
				self.form.addError("The user %s doesn't exists" % self.form.username)


		return False
