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

""" SimulationArchive.py

	This file generates the archive of the simulation

"""

from django.views.generic import TemplateView
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied

from signetsim.models import SEDMLSimulation
from signetsim.managers.simulations import exportSimulation
from os.path import basename
from django.shortcuts import redirect

class SimulationArchive(TemplateView):

	template_name = 'models/models.html'

	def __init__(self, **kwargs):
		TemplateView.__init__(self, **kwargs)

	def get(self, request, *args, **kwargs):

		if len(args) > 0:
			if SEDMLSimulation.objects.filter(id=str(args[0])).exists():

				simulation = SEDMLSimulation.objects.get(id=str(args[0]))

				if simulation.project.access == 'PU' or simulation.project.user == request.user:
					filename = exportSimulation(simulation)
					response = HttpResponse(open(filename, 'rb'), content_type='application/zip')
					response['Content-Disposition'] = 'attachment; filename=' + basename(filename)
					return response

				else:
					raise PermissionDenied
			else:
				raise Http404("Simulation doesn't exists")

		redirect('list_of_simulations')
