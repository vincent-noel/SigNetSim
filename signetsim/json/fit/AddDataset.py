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

""" GetCompartment.py

	This file...

"""

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.models import Experiment
from signetsim.managers.data import buildExperiment


class AddDataset(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)


	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		dataset_ind = int(request.POST['dataset_ind'])

		experiment_data = Experiment.objects.filter(project=self.project)[dataset_ind]
		experiment = buildExperiment(experiment_data)
		experiment_variables = experiment.getVariables()

		model_variables = {}
		model_xpaths = {}
		for variable in experiment_variables:
			if self.getModelInstance().listOfVariables.containsSbmlId(variable):
				var = self.getModelInstance().listOfVariables.getBySbmlId(variable)
				model_variables.update({variable: var.getNameOrSbmlId()})
				model_xpaths.update({variable: var.getXPath()})

			elif self.getModelInstance().listOfVariables.containsName(variable):
				var = self.getModelInstance().listOfVariables.getByName(variable)
				model_variables.update({variable: var.getNameOrSbmlId()})
				model_xpaths.update({variable: var.getXPath()})

			else:
				model_variables.update({variable: None})
				model_xpaths.update({variable: None})

		self.data.update({
			'dataset_ind': dataset_ind,
			'dataset_id': experiment_data.id,
			'dataset_name': experiment_data.name,
			'model_variables': model_variables,
			'model_xpaths': model_xpaths
		})

		return JsonRequest.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)


