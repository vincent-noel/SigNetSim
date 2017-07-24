#!/usr/bin/env python
""" ListOfModelsView.py


	This file generates the view for the list of models


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
from django.http import HttpResponse
from signetsim.views.HasWorkingProject import HasWorkingProject
from signetsim.models import Experiment
from signetsim.managers.data import exportExperiment
from os.path import basename
from django.shortcuts import redirect
from os import remove

class DataArchive(TemplateView, HasWorkingProject):

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingProject.__init__(self)

	def get_context_data(self, **kwargs):
		kwargs = HasWorkingProject.get_context_data(self, **kwargs)
		return kwargs


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
