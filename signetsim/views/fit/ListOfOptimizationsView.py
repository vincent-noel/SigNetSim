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

""" ListOfOptimizationsView.py

	This file ...

"""

from django.conf import settings
from django.views.generic import TemplateView

from libsignetsim import SbmlDocument, ModelException
from signetsim.models import SbmlModel, Optimization
from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.managers.optimizations import stopOptimization
from signetsim.managers.computations import add_computation
from time import time
from os.path import isdir, isfile, join
from shutil import rmtree
from dill import loads

class ListOfOptimizationsView(TemplateView, HasWorkingModel):

	template_name = 'fit/list_of_optimizations.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)

		self.listOfOptimizations = None


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs['optimizations'] = self.listOfOptimizations

		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingModel.isChooseModel(self, request):
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "delete_optimization":
				self.deleteOptimization(request)

			elif request.POST['action'] == "stop_optimization":
				self.stopOptimization(request)

			elif request.POST['action'] == "restart_optimization":
				self.restartOptimization(request)

		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)
		self.loadOptimizations(request)


	def deleteOptimization(self, request):

		t_optim = Optimization.objects.get(id=request.POST['entry_id'])

		if isdir(join(settings.MEDIA_ROOT,
										str(self.project.folder),
										"optimizations/optimization_%s/" % str(t_optim.optimization_id))):

			rmtree(join(settings.MEDIA_ROOT,
											str(self.project.folder),
											"optimizations/optimization_%s/" % str(t_optim.optimization_id)))

		t_optim.delete()

		self.loadOptimizations(request)


	def stopOptimization(self, request):

		t_optim = Optimization.objects.get(id=request.POST['entry_id'])
		optim_path = join(
			settings.MEDIA_ROOT,
			str(self.project.folder),
			"optimizations/optimization_%s/" % str(t_optim.optimization_id))

		if isdir(optim_path):
			stopOptimization(optim_path)

		self.loadOptimizations(request)

	def restartOptimization(self, request):

		t_optim = Optimization.objects.get(id=request.POST['entry_id'])

		add_computation(self.project, t_optim, loads(t_optim.result.encode('Latin-1')))
		self.loadOptimizations(request)


	def loadOptimizations(self, request):

		if self.list_of_models is not None and len(self.list_of_models) > 0:
			t_model = SbmlModel.objects.get(project=self.project, id=self.model_id)
			optimizations = Optimization.objects.filter(project=self.project,
										model=t_model)
			self.listOfOptimizations = []
			for optimization in optimizations:
				t_optim_id = optimization.optimization_id

				optim_path = join(settings.MEDIA_ROOT,
								str(self.project.folder),
								"optimizations/optimization_%s/" % str(t_optim_id))


				t_time_of_launch = int(time()) - (int(t_optim_id)/1000)

				t_model_name = ""
				if isfile(optim_path + "/model.sbml"):
					try:
						t_document = SbmlDocument()
						t_document.readSbmlFromFile(str(optim_path + "/model.sbml"))
						t_model_name = t_document.model.getName()
					except ModelException as e:
						t_model_name = "Unknown"

				self.listOfOptimizations.append((optimization, t_time_of_launch, t_model_name))

