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

""" ValidateEmailView.py

	This file ...

"""

from django.views.generic import TemplateView
# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError
# from django.shortcuts import redirect
# from django.core.urlresolvers import reverse_lazy
# from django.contrib.auth import authenticate, login
# from signetsim.forms import RegistrationForm, LoginForm
from signetsim.models import User
# from signetsim.views.HasErrorMessages import HasErrorMessages
# from django.core.mail import send_mail
# from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings

class ValidateEmailView(TemplateView):

	template_name = 'accounts/validate_email.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		self.verified = False

	def get_context_data(self, **kwargs):
		kwargs['verified'] = self.verified
		return kwargs


	def get(self, request, *args, **kwargs):

		if str(request.GET['username']) != "" and str(request.GET['verification_id']) != "":
			self.verifyEmail(request, str(request.GET['username']), str(request.GET['verification_id']))

		return TemplateView.get(self, request, *args, **kwargs)


	def verifyEmail(self, request, username, verification_id):
		if User.objects.filter(username=username).exists():

			t_user = User.objects.get(username=username)
			if t_user.email_verification_id == verification_id:
				t_user.is_email_verified = True
				t_user.save()
				self.verified = True
				self.sendAdminEmail(request, t_user.username, t_user.email)

	def sendAdminEmail(self, request, username, email):

		admins_email = [t_user.email for t_user in User.objects.filter(is_staff=True)]

		activate_url = "%s%saccounts/activate_account?username=%s" % (request.META['HTTP_HOST'], settings.BASE_URL, username)

		send_mail(
			subject='SigNetSim user account activation',
			message='Bad luck',
			html_message='Dear admin<br/>The user %s (%s) just registered for an account for SigNetSim. Please follow <a href="%s">this link</a> if you want to activate this account<br><br>If for some reason you cannot click this link, please copy/paste the following url in your web browser :<br/>%s<br/>' % (
							username, email, activate_url, activate_url),
			from_email='signetsim@gmail.com',
			recipient_list=admins_email,
			fail_silently=False,
		)
