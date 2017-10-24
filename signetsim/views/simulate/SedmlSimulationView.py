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

""" SedmlSimulationView.py

	This file ...

"""

from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.conf import settings
from django.http import Http404
from django.core.exceptions import PermissionDenied

from signetsim.views.HasWorkingProject import HasWorkingProject
from signetsim.views.HasErrorMessages import HasErrorMessages
from signetsim.models import SEDMLSimulation
from signetsim.settings.Settings import Settings

from libsignetsim.sedml.SedmlDocument import SedmlDocument
from libsignetsim.sedml.SedmlException import SedmlException
from os.path import join


class SedmlSimulationView(TemplateView, HasWorkingProject, HasErrorMessages):

	template_name = 'simulate/sedml_simulation.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingProject.__init__(self)
		HasErrorMessages.__init__(self)
		self.listOfPlots2D = None


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingProject.get_context_data(self, **kwargs)
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)
		kwargs['plots_2d'] = self.listOfPlots2D
		kwargs['colors'] = Settings.default_colors

		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		if len(args) > 0:
			self.loadSedmlSimulation(request, int(args[0]))

		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingProject.isChooseProject(self, request):
				return redirect('list_of_simulations')

		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):
		HasWorkingProject.load(self, request, *args, **kwargs)
		HasErrorMessages.clearErrors(self)

	def loadSedmlSimulation(self, request, sedml_id):

		if SEDMLSimulation.objects.filter(id=sedml_id).exists():
			sedml_file = SEDMLSimulation.objects.get(id=sedml_id)

			if sedml_file.project.user == request.user or sedml_file.project.access == "PU":
				try:
					sedml_doc = SedmlDocument()
					sedml_doc.readSedmlFromFile(join(settings.MEDIA_ROOT, str(sedml_file.sedml_file)))
					sedml_doc.run()
					self.listOfPlots2D = sedml_doc.listOfOutputs.getPlots2D()

				except SedmlException as e:
					self.addError("Invalid SEDML document : " + e.message)

			else:
				raise PermissionDenied

		else:
			raise Http404("The simulation doesn't exist !")