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

""" ActivateAccountView.py

	This file ...

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

			self.sendUserEmail(request, t_user.username, t_user.email)
			self.activated = True

		return TemplateView.get(self, request, *args, **kwargs)

	def sendUserEmail(self, request, username, email):

		url = settings.BASE_URL
		if "HTTP_X_SCRIPT_NAME" in request.META and request.META['HTTP_X_SCRIPT_NAME'] != "":
			url = str(request.META['HTTP_X_SCRIPT_NAME']) + url

		if "HTTP_X_SCHEME" in request.META and request.META['HTTP_X_SCHEME'] != "":
			url = "%s://%s%s" % (str(request.META['HTTP_X_SCHEME']), request.META['HTTP_HOST'], url)

		else:
			url = "%s://%s%s" % (request.scheme, request.META['HTTP_HOST'], url)

		login_url = "%saccounts/login/" % url

		send_mail(
			subject='SigNetSim user account activated',
			message='',
			html_message='Dear %s, <br/><br/>Your SigNetSim account has just been activated ! <br>You can start using it right now, by going to the page <br/>%s<br/>' % (
							username, login_url),
			from_email='signetsim@gmail.com',
			recipient_list=[email],
			fail_silently=True,
		)