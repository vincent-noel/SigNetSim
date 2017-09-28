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

""" SignUpView.py

	This file ...

"""

from django.views.generic import TemplateView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
# from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
# from signetsim.forms import RegistrationForm, LoginForm
from signetsim.models import User
from signetsim.views.HasErrorMessages import HasErrorMessages
from django.core.mail import send_mail
from django.conf import settings

class SignUpForm(HasErrorMessages):

	def __init__(self, parent_view):

		HasErrorMessages.__init__(self)

		self.parent_view = parent_view
		self.username = None
		self.firstname = None
		self.lastname = None
		self.email = None
		self.organisation = None
		self.password1 = None
		self.password2 = None

	def read(self, request):

		self.username = self.readString(request, 'username', 'the username')
		self.firstname = self.readUnicodeString(request, 'first_name', 'the first name', required=False)
		self.lastname = self.readUnicodeString(request, 'last_name', 'the last name', required=False)
		self.email = self.readString(request, 'email', 'the email address')
		self.organisation = self.readString(request, 'organization', 'the organisation')
		self.password1 = self.readString(request, 'password1', 'the password')
		self.password2 = self.readString(request, 'password2', 'the password confirmation')

		if self.password1 != self.password2:
			self.addError("The two passwords are different !")

		try:
			validate_email(self.email)
		except ValidationError:
			self.addError("Invalid email address")

class SignUpView(TemplateView):

	template_name = 'accounts/signup.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		self.form = SignUpForm(self)


	def get_context_data(self, **kwargs):

		kwargs = HasErrorMessages.get_context_data(self.form, **kwargs)
		kwargs['form'] = self.form
		return kwargs


	def get(self, request, *args, **kwargs):
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		if "action" in request.POST:
			if request.POST['action'] == "signup":
				if self.signup(request) is True:
					return redirect('signup_success')

		return TemplateView.get(self, request, *args, **kwargs)


	def signup(self, request):

		request.session['signup_username'] = ""
		request.session['signup_email'] = ""

		self.form.read(request)
		if not self.form.hasErrors():
			if User.objects.filter(username=self.form.username).exists():
				self.form.addError("Username %s already exists !" % self.form.username)
				return False
			else:
				user = User.objects.create_user(self.form.username, self.form.email, self.form.password1)
				user.first_name = self.form.firstname
				user.last_name = self.form.lastname
				user.organization = self.form.organisation
				user.is_active = False
				user.save()
				request.session['signup_username'] = self.form.username
				request.session['signup_email'] = self.form.email

				# For test runs
				if 'HTTP_HOST' in request.META:
					self.sendAdminEmail(request, self.form.username, self.form.email)
				return True
		return False

	# def sendActivationEmail(self, request, verification_id):
	#
	#     validation_url = "%s%saccounts/validate_email?username=%s&verification_id=%s" % (request.META['HTTP_HOST'], settings.BASE_URL, self.form.username, verification_id)
	#     full_message = ("Dear %s, <br/>You just registered for an account for SigNetSim. Please click on this <a href=\"http://%s\">link</a> to activate your account.<br>" % (
	#                     self.form.username, validation_url)
	#                     + "<br><br>If for some reason you cannot click this link, please copy/paste the following url in your web browser :<br/>http://%s<br/>" % (validation_url))
	#     send_mail(
	#         subject='SigNetSim email verification',
	#         message='',
	#         html_message=full_message,
	#         from_email='signetsim@gmail.com',
	#         recipient_list=[self.form.email],
	#         fail_silently=False,
	#     )


	def sendAdminEmail(self, request, username, email):

		admins_email = [t_user.email for t_user in User.objects.filter(is_staff=True)]

		url = settings.BASE_URL
		if request.META['HTTP_X_SCRIPT_NAME'] != "":
			url = str(request.META['HTTP_X_SCRIPT_NAME']) + url

		if request.META['HTTP_X_SCHEME'] != "":
			url = "%s://%s%s" % (str(request.META['HTTP_X_SCHEME']), request.META['HTTP_HOST'], url)

		else:
			url = "%s://%s%s" % (request.scheme, request.META['HTTP_HOST'], url)

		activate_url = "%saccounts/activate_account?username=%s" % (url, username)

		send_mail(
			subject='SigNetSim user account activation',
			message='',
			html_message='Dear admin<br/>The user %s (%s) just registered for an account for SigNetSim. Please follow <a href="%s">this link</a> if you want to activate this account<br><br>If for some reason you cannot click this link, please copy/paste the following url in your web browser :<br/>%s<br/>' % (
							username, email, activate_url, activate_url),
			from_email='signetsim@gmail.com',
			recipient_list=admins_email,
			fail_silently=True,
		)


class SignUpSuccessView(TemplateView):

	template_name = 'accounts/signup_success.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)


	def get_context_data(self, **kwargs):
		return kwargs


	def get(self, request, *args, **kwargs):
		return TemplateView.get(self, request, *args, **kwargs)
