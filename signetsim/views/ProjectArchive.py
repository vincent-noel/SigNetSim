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

""" ProjectArchive.py

	This file generates the view for the list of models

"""

from django.views.generic import TemplateView
from django.http import HttpResponse, Http404, HttpResponseForbidden
from signetsim.models import Project
from signetsim.managers.projects import exportProject
from os.path import basename
from django.shortcuts import redirect

class ProjectArchive(TemplateView):

	template_name = 'models/models.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)

	def get(self, request, *args, **kwargs):

		if len(args) > 0:
			if Project.objects.filter(folder=str(args[0])).exists():

				project = Project.objects.get(folder=str(args[0]))

				if project.access == 'PU' or project.user == request.user:
					filename = exportProject(project)
					response = HttpResponse(open(filename, 'rb'), content_type='application/zip')
					response['Content-Disposition'] = 'attachment; filename=' + basename(filename)
					return response

				else:
					raise HttpResponseForbidden
			else:
				raise Http404("Project doesn't exists")

		redirect('projects')
