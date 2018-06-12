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
from signetsim.models import User
from signetsim.views.HasErrorMessages import HasErrorMessages
from signetsim.managers.users import deleteUser

class UsersView(TemplateView, HasErrorMessages):
	template_name = 'admin/users.html'


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

			elif request.POST['action'] == "save_quotas":
				self.saveQuotas(request)
		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):
		self.users = User.objects.all()

	def deleteUser(self, request):

		if User.objects.filter(id=int(request.POST['id'])).exists():

			user = User.objects.get(id=int(request.POST['id']))
			deleteUser(user)

	def saveQuotas(self, request):
		if (
			User.objects.filter(username=request.POST['username']).exists() and
			"user_cores" in request.POST and request.POST["user_cores"] != "" and
			"user_cpu_time" in request.POST and request.POST["user_cpu_time"] != ""
			"user_used_cpu_time" in request.POST and request.POST["user_used_cpu_time"] != ""
		):
			user = User.objects.get(username=request.POST['username'])
			user.max_cores = int(request.POST["user_cores"])
			user.max_cpu_time = int(request.POST["user_cpu_time"])
			user.used_cpu_time = float(request.POST["user_used_cpu_time"])

			user.save()
