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
from signetsim.models import Project, SbmlModel, SEDMLSimulation, CombineArchiveModel
from libsignetsim.combine.CombineArchive import CombineArchive
from django.conf import settings
from os.path import join, basename, isfile
from os import remove
from django.shortcuts import redirect
from django.core.files import File
from libsignetsim.settings.Settings import Settings

class GenerateCombineArchive(TemplateView):

	template_name = 'models/models.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)

	def get_context_data(self, **kwargs):
		return kwargs


	def get(self, request, *args, **kwargs):

		if len(args) > 0:
			filename = self.generateCombineArchive(request, args[0])

			response = HttpResponse(open(filename, 'rb'), content_type='application/zip')
			response['Content-Disposition'] = 'attachment; filename=' + basename(filename)
			return response

		redirect('projects')

	def generateCombineArchive(self, request, project_id):

		projects = Project.objects.filter(user=request.user)
		project = projects[int(project_id)]

		combine_archive = CombineArchive()
		for sbml_model in SbmlModel.objects.filter(project=project):
			combine_archive.addFile(join(settings.MEDIA_ROOT, str(sbml_model.sbml_file)))

		for sedml_model in SEDMLSimulation.objects.filter(project=project):
			combine_archive.addFile(join(settings.MEDIA_ROOT, str(sedml_model.sedml_file)))

		filename = ''.join(e for e in project.name if e.isalnum()) + ".omex"
		filename = join(Settings.tempDirectory, filename)
		combine_archive.writeArchive(filename)

		archive = None
		if len(CombineArchiveModel.objects.filter(project=project)) == 0:
			archive = CombineArchiveModel(project=project, archive_file=File(open(filename, 'r')))
			archive.name = project.name
			archive.save()
		else:
			archive = CombineArchiveModel.objects.get(project=project)
			t_filename = join(settings.MEDIA_ROOT, str(archive.archive_file))
			if isfile(t_filename) and filename != t_filename:
				remove(t_filename)
				archive.archive_file = File(open(filename))
				archive.save()


		return join(settings.MEDIA_ROOT, str(archive.archive_file))