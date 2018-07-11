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

""" AdminView.py

	This file ...

"""

from django.views.generic import TemplateView
from django.conf import settings
from signetsim.models import User
from signetsim.views.HasErrorMessages import HasErrorMessages
from signetsim.managers.users import deleteUser

class SettingsView(TemplateView, HasErrorMessages):
	template_name = 'admin/settings.html'

	def __init__(self, **kwargs):
		TemplateView.__init__(self, **kwargs)
		HasErrorMessages.__init__(self)

		# "email_address": "signetsim@gmail.com",
		# "email_use_tls": true,
		# "email_host": "smtp.gmail.com",
		# "email_port": "587",
		# "email_user": "signetsim",
		# "email_password": "poil0cu!",

		self.mailAddress = None
		self.mailUseTLS = None
		self.mailHost = None
		self.mailPort = None
		self.mailUser = None

	def get_context_data(self, **kwargs):
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)
		kwargs['mail_address'] = self.mailAddress
		kwargs['mail_use_tls'] = self.mailUseTLS
		kwargs['mail_host'] = self.mailHost
		kwargs['mail_port'] = self.mailPort
		kwargs['mail_user'] = self.mailUser
		kwargs['mail_active'] = (
			self.mailAddress != None and
			self.mailHost != None and
			self.mailPort!= None and
			self.mailUser != None
		)
		return kwargs

	def get(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)
		if "action" in request.POST:
			pass

		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):
		self.mailAddress = settings.EMAIL_ADDRESS
		self.mailUseTLS = settings.EMAIL_USE_TLS
		self.mailHost = settings.EMAIL_HOST
		self.mailPort = settings.EMAIL_PORT
		self.mailUser = settings.EMAIL_HOST_USER

	def deleteUser(self, request):

		if User.objects.filter(id=int(request.POST['id'])).exists():
			user = User.objects.get(id=int(request.POST['id']))
			deleteUser(user)

