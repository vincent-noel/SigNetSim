#!/usr/bin/env python
""" HasUserLoggedIn.py


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

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from signetsim.models import SbmlModel

from libsignetsim.model.Model import Model
from libsignetsim.model.ModelException import ModelException
# from signetsim.views.HasWorkingProject import HasWorkingProject
import os

class HasUserLoggedIn(object):

	def isUserLoggedIn(self, request):
		return not request.user.is_anonymous()
