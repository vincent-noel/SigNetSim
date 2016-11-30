#!/usr/bin/env python
""" DataOptimizationView.py


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

from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.models import Optimization
from signetsim.models import Experiment, Condition
from signetsim.models import Observation, Treatment
from signetsim.views.fit.DataOptimizationForm import DataOptimizationForm
from libsignetsim.data.Experiment import Experiment as SigNetSimExperiment
from libsignetsim.data.ExperimentalCondition import ExperimentalCondition
from libsignetsim.data.ListOfExperimentalData import ListOfExperimentalData
from libsignetsim.data.ExperimentalData import ExperimentalData

from libsignetsim.optimization.ModelVsTimeseriesOptimization import ModelVsTimeseriesOptimization

import threading
import os
import json


class DataOptimizationView(TemplateView, HasWorkingModel):

	template_name = 'fit/data_v2.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)

		self.form = DataOptimizationForm(self)

	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)

		kwargs['experimental_data_sets'] = Experiment.objects.filter(project=self.project)
		kwargs['list_of_species'] = self.model.listOfSpecies.values()
		kwargs['ids_of_species'] = self.model.listOfSpecies.sbmlIds()
		kwargs['selected_datasets'] = self.form.selectedDataSets
		kwargs['selected_datasets_ids'] = self.form.selectedDataSetsIds
		kwargs['selected_parameters'] = self.form.selectedParameters

		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if self.isChooseModel(request):
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "add_dataset":
				self.form.addDataset(request)

			elif request.POST['action'] == "remove_dataset":
				self.form.removeDataset(request)

			elif request.POST['action'] == "create":
				self.runOptimization(request)



		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.form.loadParameters(request)


	def runOptimization(self, request):

		self.form.readSelectedDataset(request)
		self.form.loadMapping(request)

		experiments = self.form.buildExperiments(request)
		return
		t_optimization = ModelVsTimeseriesOptimization(
							workingModel = self.model,
							list_of_experiments = experiments,
							mapping=self.speciesMapping,
							parameters_to_fit=self.selectedParameters)
		t_optimization.setTempDirectory(os.path.join(settings.MEDIA_ROOT, str(self.project.folder), "optimizations"))
		nb_procs = 1

		print "calling writeOptimizationFiles from the view"
		t_optimization.writeOptimizationFiles(nb_procs)
		print "view is done"
		t = threading.Thread(group=None,
								target=t_optimization.runOptimization,
								args=(nb_procs, None, None, ))

		t.setDaemon(True)
		t.start()

		new_optimization = Optimization(project=self.project,
								model=self.list_of_models[self.model_id],
								optimization_id=t_optimization.optimizationId)
		new_optimization.save()
