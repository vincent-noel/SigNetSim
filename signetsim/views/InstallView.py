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

""" InstallView.py

	This file is the installation script. It will create an admin user, and create the Settings object

"""

from django.views.generic import TemplateView
from django.conf import settings as django_settings
from signetsim.models import User, Settings
from os import utime
from os.path import join
from threading import Thread


class InstallView(TemplateView):
	template_name = 'install.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		self.install_done = False


	def get_context_data(self, **kwargs):

		kwargs['install_done'] = self.install_done
		return kwargs


	def post(self, request, *args, **kwargs):

		username = request.POST.get('admin_username')
		email = request.POST.get('admin_email')
		password1 = request.POST.get('admin_password1')
		password2 = request.POST.get('admin_password2')

		email_active = request.POST.get('mail_active') == "on"
		email_address = request.POST.get('email_address')
		email_host = request.POST.get('email_host')
		email_port = request.POST.get('email_port')
		email_tls = request.POST.get('email_tls') == "on"
		email_username = request.POST.get('email_username')
		email_password = request.POST.get('email_password')

		if username is not None and email is not None and password1 is not None and password1 == password2:
			admin = User.objects.create_superuser(username, email, password1)

			if (email_active
				and email_address != "" and email_host != "" and email_port != ""
				and email_username != "" and email_password != ""
			):

				settings = Settings(
					base_url=request.META['PATH_INFO'],
					admin=admin,
					email_address=email_address,
					email_use_tls=email_tls,
					email_host=email_host,
					email_port=int(email_port),
					email_user=email_username,
					email_password=email_password
				)
			else:
				settings = Settings(
					base_url=request.META['PATH_INFO'],
					admin=admin,
				)
			settings.save()

			thread = ReloadConf()
			thread.start()
			self.install_done = True
		return TemplateView.get(self, request, *args, **kwargs)


class ReloadConf(Thread):

	"""Thread just to reload the django conf after returning the page"""

	def __init__(self):
		Thread.__init__(self)

	def run(self):
		utime(join(django_settings.BASE_DIR, "signetsim/settings/default.py"), None)
		utime(join(django_settings.BASE_DIR, "signetsim/settings/apache.py"), None)
		utime(join(django_settings.BASE_DIR, "signetsim/settings/wsgi.py"), None)

