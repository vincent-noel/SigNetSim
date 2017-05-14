#!/usr/bin/env python
""" ListOfSimulationsView.py


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

from django.views.generic import TemplateView
from signetsim.views.HasWorkingProject import HasWorkingProject
from signetsim.models import SEDMLSimulation
from libsignetsim.sedml.SedmlDocument import SedmlDocument
from django.conf import settings
from signetsim.settings.Settings import Settings
from os.path import join

class SedmlSimulationView(TemplateView, HasWorkingProject):

	template_name = 'simulate/sedml_simulation.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingProject.__init__(self)

		self.listOfPlots2D = None


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingProject.get_context_data(self, **kwargs)
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
				self.load(request, *args, **kwargs)

		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):
		HasWorkingProject.load(self, request, *args, **kwargs)

	def loadSedmlSimulation(self, request, sedml_id):

		sedml_files = SEDMLSimulation.objects.filter(project=self.project)
		if sedml_id < len(sedml_files):
			sedml_file = sedml_files[sedml_id]
			sedml_doc = SedmlDocument()
			sedml_doc.readSedmlFromFile(join(settings.MEDIA_ROOT, str(sedml_file.sedml_file)))
			sedml_doc.run()
			self.listOfPlots2D = sedml_doc.listOfOutputs.getPlots2D()


