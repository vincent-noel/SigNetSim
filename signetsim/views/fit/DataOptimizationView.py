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

""" DataOptimizationView.py

	This file ...

"""

from django.views.generic import TemplateView

from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.models import Optimization, SbmlModel, Experiment
from .DataOptimizationForm import DataOptimizationForm

from libsignetsim import ModelVsTimeseriesOptimization, LibSigNetSimException

from threading import Thread
from os.path import isdir, join
from os import mkdir


class DataOptimizationView(TemplateView, HasWorkingModel):

	template_name = 'fit/data.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)

		self.form = DataOptimizationForm(self)

	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)

		kwargs['experimental_data_sets'] = [experiment.name for experiment in Experiment.objects.filter(project=self.project)]
		kwargs['list_of_species'] = self.getModelInstance().listOfSpecies
		kwargs['list_of_parameters'] = self.getModelInstance().listOfParameters
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

			elif request.POST['action'] == "create":
				self.runOptimization(request)

		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.form.loadParameters(request)


	def runOptimization(self, request):

		try:
			self.form.read(request)

			t_parameters = []

			for (ind, active, name, value, vmin, vmax, precision) in self.form.selectedParameters:

				if active:
					if ind < len(self.getModelInstance().listOfParameters):
						t_parameter = self.getModelInstance().listOfParameters.getByPos(ind)
					else:
						i_parameter = len(self.getModelInstance().listOfParameters)
						i_reaction = 0
						while (i_parameter + len(self.getModelInstance().listOfReactions.getByPos(i_reaction).listOfLocalParameters)) < ind:
							i_parameter += len(self.getModelInstance().listOfReactions.getByPos(i_reaction).listOfLocalParameters)
							i_reaction += 1
						t_parameter = self.getModelInstance().listOfReactions.getByPos(i_reaction).listOfLocalParameters.getByPos(ind-i_parameter)

					if self.getModelInstance().parentDoc.isCompEnabled():
						t_parameter = self.getModelInstance().getDefinitionVariable(t_parameter)[0]

					t_parameters.append((t_parameter, value, vmin, vmax, precision))

			if len(t_parameters) == 0:
				self.form.addError("Please select at least one parameter to optimize.")

			if len(self.form.selectedExperiments) == 0:
				self.form.addError("Please select at least one experiment to use as reference for the fit.")


			if len(t_parameters) > 0 and len(self.form.selectedExperiments) > 0:

				# experiments = self.form.buildExperiments(request)
				t_optimization = ModelVsTimeseriesOptimization(
									workingModel=self.model,
									list_of_experiments=self.form.selectedExperiments,
									parameters_to_fit=t_parameters,
									mapping=self.form.mappings,
									nb_procs=self.form.nbCores,
									p_lambda=self.form.plsaLambda,
									p_criterion=self.form.plsaCriterion,
									p_precision=self.form.plsaPrecision,
									p_initial_temperature=self.form.plsaInitialTemperature,
									p_initial_moves=self.form.plsaInitialMoves,
									p_freeze_count=self.form.plsaFreezeCount,
									s_neg_penalty=self.form.scoreNegativePenalty
				)

				if not isdir(join(self.getProjectFolder(), "optimizations")):
					mkdir(join(self.getProjectFolder(), "optimizations"))

				t_optimization.setTempDirectory(join(self.getProjectFolder(), "optimizations"))
				nb_procs = 2

				t = Thread(group=None,
										target=t_optimization.runOptimization,
										args=(nb_procs, None, None, ))

				t.setDaemon(True)
				t.start()

				t_model = SbmlModel.objects.get(id=self.model_id)

				new_optimization = Optimization(project=self.project,
										model=t_model,
										optimization_id=t_optimization.optimizationId)
				new_optimization.save()


		except LibSigNetSimException as e:
			self.form.addError(e.message)

