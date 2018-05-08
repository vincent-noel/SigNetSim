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

""" DataOptimizationForm.py

	This file ...

"""

from signetsim.models import Experiment
from signetsim.views.HasErrorMessages import HasErrorMessages
from signetsim.managers.data import buildExperiment

from libsignetsim import Settings


class DataOptimizationForm(HasErrorMessages):

	def __init__(self, view):

		HasErrorMessages.__init__(self)
		self.view = view

		self.selectedDataSetsIds = None
		self.selectedExperiments = None

		self.speciesMapping = None
		self.selectedParameters = None

		self.nbCores = 2
		self.plsaLambda = Settings.defaultPlsaLambda
		self.plsaCriterion = Settings.defaultPlsaCriterion
		self.plsaPrecision = Settings.defaultPlsaPrecision
		self.plsaInitialTemperature = Settings.defaultPlsaInitialTemperature
		self.plsaInitialMoves = Settings.defaultPlsaInitialMoves
		self.plsaFreezeCount = Settings.defaultPlsaFreezeCount
		self.scoreNegativePenalty = Settings.defaultScoreNegativePenalty

		self.mappings = []

	def read(self, request):
		self.readSelectedDataset(request)
		self.loadMapping(request)
		self.readSettings(request)

	def readSettings(self, request):
		self.nbCores = self.readInt(request, 'nb_cores', "the number of cores")
		self.plsaLambda = self.readFloat(request, 'lambda', "the lambda setting")
		self.plsaCriterion = self.readFloat(request, 'score_precision', "the score function precision setting")
		self.plsaPrecision = self.readInt(request, 'param_precision', "the parameter precision setting")
		self.plsaInitialTemperature = self.readFloat(request, 'initial_temperature', "the initial temperature setting")
		self.plsaInitialMoves = self.readFloat(request, 'initial_moves', "the initial moves setting")
		self.plsaFreezeCount = self.readFloat(request, 'freeze_count', "the freeze count setting")
		self.scoreNegativePenalty = self.readFloat(request, 'negative_penalty', "the negative penalty setting")

	def readSelectedDataset(self, request):

		self.selectedDataSetsIds = []
		self.selectedExperiments = []

		i_dataset_selected = 0

		while ("dataset_%d" % i_dataset_selected) in request.POST:
			t_id = int(request.POST["dataset_%d" % i_dataset_selected])
			self.selectedDataSetsIds.append(t_id)
			self.selectedExperiments.append(buildExperiment(Experiment.objects.get(id=t_id)))
			i_dataset_selected += 1

	def loadMapping(self, request):

		ind_dataset = 0
		ind_species = 0

		self.mappings = []
		while "list_dataset_%d_species_%d_value" % (ind_dataset, ind_species) in request.POST:

			mapping = {}
			while "list_dataset_%d_species_%d_value" % (ind_dataset, ind_species) in request.POST:

				data_species = request.POST['list_dataset_%d_data_species_%d_value' % (ind_dataset, ind_species)]
				species = request.POST['list_dataset_%d_species_%d_value' % (ind_dataset, ind_species)]

				if len(str(species)) > 0:
					mapping.update({data_species: self.view.getModelInstance().listOfSpecies[int(species)].getXPath()})
				ind_species += 1

			self.mappings.append(mapping)
			ind_dataset += 1

	def loadParameters(self, request):

		self.selectedParameters = []

		if "parameter_0_id" not in request.POST:

			# Default parameters
			i_parameter = 0
			for parameter in self.view.getModelInstance().listOfParameters:
				if parameter.getValue() is not None:
					self.selectedParameters.append(
						(
							i_parameter, True,
							parameter.getNameOrSbmlId(),
							parameter.getValue(),
							parameter.getValue()*1e-4,
							parameter.getValue()*1e4,
							Settings.defaultPlsaPrecision))

					i_parameter += 1

			for reaction in self.view.getModelInstance().listOfReactions:
				for parameter in reaction.listOfLocalParameters:
					if parameter.getValue() is not None:
						self.selectedParameters.append(
							(
								i_parameter, True,
								parameter.getNameOfSbmlId(),
								parameter.getValue(),
								parameter.getValue()*1e-4,
								parameter.getValue()*1e4,
								Settings.defaultPlsaPrecision))


		else:
			i_parameter = 0
			while ("parameter_%d_id" % i_parameter) in request.POST:

				t_active = self.readOnOff(
					request, 'parameter_%d_active' % i_parameter,
					"the status of the parameter #%d" % i_parameter
				)

				t_name = self.readASCIIString(
					request, 'parameter_%d_name' % i_parameter,
					"the name of the parameter #%d" % i_parameter
				)

				if t_active:

					t_value = self.readFloat(
						request, "parameter_%d_value" % i_parameter,
						"the value of the parameter #%d" % i_parameter
					)

					t_min = self.readFloat(
						request, "parameter_%d_min" % i_parameter,
						"the minimum value of the parameter #%d" % i_parameter
					)

					t_max = self.readFloat(
						request, "parameter_%d_max" % i_parameter,
						"the maximum value of the parameter #%d" % i_parameter
					)

					t_precision = self.readInt(
						request, "parameter_%d_precision" % i_parameter,
								 "the number of significant figures of the parameter #%d" % i_parameter
					)

					self.selectedParameters.append(
						(i_parameter, t_active, t_name, t_value, t_min, t_max, t_precision)
					)

				i_parameter += 1
