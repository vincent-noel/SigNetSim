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

""" DataArchive.py

	This file generates the view for the list of models

"""

from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import redirect

from signetsim.views.HasWorkingProject import HasWorkingProject
from signetsim.models import Experiment
from signetsim.managers.data import exportExperiment

from os import remove
from os.path import basename


class DataArchive(TemplateView, HasWorkingProject):

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingProject.__init__(self)

	def get(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)

		if len(args) > 0:

			experiment = Experiment.objects.get(project=self.project, id=int(args[0]))
			filename = exportExperiment(experiment)

			response = HttpResponse(open(filename, 'rb'), content_type='text/xml')
			response['Content-Disposition'] = 'attachment; filename=' + basename(filename)
			remove(filename)

			return response

		redirect('experimental_data')
