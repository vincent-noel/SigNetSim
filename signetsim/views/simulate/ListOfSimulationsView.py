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
from django.conf import settings
from signetsim.views.HasWorkingProject import HasWorkingProject
from signetsim.models import SEDMLSimulation
from signetsim.forms import DocumentForm
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.sedml.SedmlDocument import SedmlDocument
from os.path import join, basename
from os import remove


class ListOfSimulationsView(TemplateView, HasWorkingProject):

	template_name = 'simulate/list_of_simulations.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingProject.__init__(self)

		self.listOfSimulations = None
		self.fileUploadForm = DocumentForm()


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingProject.get_context_data(self, **kwargs)
		kwargs['list_of_simulations'] = self.listOfSimulations
		kwargs['load_simulation_form'] = self.fileUploadForm

		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingProject.isChooseProject(self, request):
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "delete_simulation":
				self.deleteSimulation(request)

			elif request.POST['action'] == "load_simulation":
				self.loadSimulation(request)

		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)
		self.loadListOfSimulations()

	def loadListOfSimulations(self):
		self.listOfSimulations = []

		for simulation in SEDMLSimulation.objects.filter(project=self.project):
			self.listOfSimulations.append((simulation.name, str(simulation.sedml_file)))

	def deleteSimulation(self, request):

		if 'id' in request.POST and request.POST['id'] != "":
			t_simulation = SEDMLSimulation.objects.filter(project=self.project)[int(request.POST['id'])]
			remove(join(settings.MEDIA_ROOT, str(t_simulation.sedml_file)))
			t_simulation.delete()
			self.loadListOfSimulations()


	def loadSimulation(self, request):

		self.fileUploadForm = DocumentForm(request.POST, request.FILES)
		if self.fileUploadForm.is_valid():

			sedml_archive = SEDMLSimulation(project=self.project, sedml_file=request.FILES['docfile'])
			sedml_archive.name = basename(str(request.FILES['docfile'])).split('.')[0]
			sedml_archive.save()

			# Now everything is in the same folder
			sedml_doc = SedmlDocument()
			sedml_doc.readSedmlFromFile(join(settings.MEDIA_ROOT, str(sedml_archive.sedml_file)))
			sedml_doc.listOfModels.removePaths()

			sbml_files = sedml_doc.listOfModels.makeLocalSources()

			for sbml_file in sbml_files:

				if len(SbmlModel.objects.filter(project=self.project, sbml_file=join(join(str(self.project.folder), "models"), basename(sbml_file)))) == 0:

					t_file = File(open(sbml_file, 'r'))
					sbml_model = SbmlModel(project=self.project, sbml_file=t_file)
					sbml_model.save()
					try:
						doc = SbmlDocument()

						doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(sbml_model.sbml_file)))

						sbml_model.name = doc.model.getName()
						sbml_model.save()
					except ModelException:
						name = os.path.splitext(str(sbml_model.sbml_file))[0]
						sbml_model.name = name
						sbml_model.save()

			sedml_doc.writeSedmlToFile(join(settings.MEDIA_ROOT, str(sedml_archive.sedml_file)))
			self.loadListOfSimulations()

