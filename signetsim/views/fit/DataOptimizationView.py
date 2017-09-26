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

from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.models import Optimization, SbmlModel, Experiment
from signetsim.views.fit.DataOptimizationForm import DataOptimizationForm

from libsignetsim.optimization.ModelVsTimeseriesOptimization import ModelVsTimeseriesOptimization

import threading

from os.path import isdir, join
from os import mkdir


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
		kwargs['list_of_parameters'] = self.model.listOfParameters.values()
		kwargs['ids_of_species'] = self.model.listOfSpecies.sbmlIds()
		kwargs['selected_datasets'] = self.form.selectedDataSets
		kwargs['selected_datasets_ids'] = self.form.selectedDataSetsIds
		kwargs['selected_parameters'] = self.form.selectedParameters

		kwargs['form'] = self.form
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
		self.form.readSettings(request)

		t_parameters = []
		for (ind, active, name, value, vmin, vmax) in self.form.selectedParameters:

			if active:
				t_parameter = None
				if ind < self.model.listOfParameters:
					t_parameter = self.model.listOfParameters.getByPos(ind)
				else:
					i_parameter = len(self.model.listOfParameters)
					i_reaction = 0
					while (i_parameter + len(self.model.listOfReactions.getByPos(i_reaction).listOfLocalParameters)) < ind:
						i_parameter += len(self.model.listOfReactions.getByPos(i_reaction).listOfLocalParameters)
						i_reaction += 1
					t_parameter = self.model.listOfReactions.getByPos(i_reaction).listOfLocalParameters.getByPos(ind-i_parameter)

				t_parameters.append((t_parameter, value, vmin, vmax))


		experiments = self.form.buildExperiments(request)
		t_optimization = ModelVsTimeseriesOptimization(
							workingModel=self.model,
							list_of_experiments=experiments,
							parameters_to_fit=t_parameters,
							nb_procs=self.form.nbCores,
							p_lambda=self.form.plsaLambda,
							p_criterion=self.form.plsaCriterion,
							p_initial_temperature=self.form.plsaInitialTemperature,
							p_initial_moves=self.form.plsaInitialMoves,
							s_neg_penalty=self.form.scoreNegativePenalty
		)

		if not isdir(join(self.getProjectFolder(), "optimizations")):
			mkdir(join(self.getProjectFolder(), "optimizations"))

		t_optimization.setTempDirectory(join(self.getProjectFolder(), "optimizations"))
		nb_procs = 2

		t = threading.Thread(group=None,
								target=t_optimization.runOptimization,
								args=(nb_procs, None, None, ))

		t.setDaemon(True)
		t.start()

		t_model = SbmlModel.objects.get(id=self.model_id)

		new_optimization = Optimization(project=self.project,
								model=t_model,
								optimization_id=t_optimization.optimizationId)
		new_optimization.save()
