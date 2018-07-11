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

""" HasUserLoggedIn.py

	This file ...

"""
from django import __version__
from signetsim.managers.computations import updateComputationTime
from signetsim.settings.Settings import Settings

class HasUserLoggedIn(object):

	def isUserLoggedIn(self, request):
		if int(__version__.split('.')[0]) < 2:
			return not request.user.is_anonymous()
		else:
			return not request.user.is_anonymous

	def hasCPUTimeQuota(self, request):
		if self.isUserLoggedIn(request):
			return request.user.used_cpu_time < request.user.max_cpu_time
		else:
			return True

	def getCPUTimeQuota(self, request):
		if self.isUserLoggedIn(request):
			return (request.user.max_cpu_time - request.user.used_cpu_time) * 3600
		else:
			return Settings.maxVisitorCPUTime

	def addCPUTime(self, request, time):
		if self.isUserLoggedIn(request):
			updateComputationTime(request.user, time)
