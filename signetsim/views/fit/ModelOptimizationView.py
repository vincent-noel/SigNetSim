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

""" ModelOptimizationView.py

	This file ...

"""

from django.views.generic import TemplateView
from signetsim.views.HasWorkingModel import HasWorkingModel

class ModelOptimizationView(TemplateView, HasWorkingModel):

	template_name = 'fit/model.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)

		return kwargs


	def get(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)

		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)

		if "action" in request.POST:
			if self.isChooseModel(request):
				# Already done !
				pass

		return TemplateView.get(self, request, *args, **kwargs)
