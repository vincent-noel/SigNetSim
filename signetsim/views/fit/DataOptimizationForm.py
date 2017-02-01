#!/usr/bin/env python
""" DataOptimizationForm.py


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

from libsignetsim.data.Experiment import Experiment as SigNetSimExperiment
from libsignetsim.data.ExperimentalCondition import ExperimentalCondition
from libsignetsim.data.ListOfExperimentalData import ListOfExperimentalData
from libsignetsim.data.ExperimentalData import ExperimentalData

from libsignetsim.optimization.ModelVsTimeseriesOptimization import ModelVsTimeseriesOptimization

import threading
import os
import json


class DataOptimizationForm(object):

	def __init__(self, view, **kwargs):

		self.view = view

		self.selectedDataSets = None
		self.selectedDataSetsIds = None

		self.speciesMapping = None
		self.selectedParameters = None


	def removeDataset(self, request):

		self.readSelectedDataset(request)
		self.selectedDataSetsIds.remove(int(request.POST['dataset_id']))
		self.loadMapping(request)


	def addDataset(self, request):

		self.readSelectedDataset(request)

		datasets = Experiment.objects.filter(project=self.view.project)
		dataset_id = datasets[int(request.POST['dataset_id'])].id

		self.selectedDataSetsIds.append(dataset_id)
		self.selectedDataSetsIds = list(set(self.selectedDataSetsIds))

		self.loadMapping(request)
		print self.selectedDataSets
		print self.selectedDataSetsIds

	def readSelectedDataset(self, request):

		self.selectedDataSetsIds = []
		i_dataset_selected = 0

		while ("dataset_%d" % i_dataset_selected) in request.POST:
			self.selectedDataSetsIds.append(
				int(request.POST["dataset_%d" % i_dataset_selected]))

			i_dataset_selected += 1


	def loadMapping(self, request):

		self.selectedDataSets = []
		for i, t_id in enumerate(self.selectedDataSetsIds):
			self.selectedDataSets.append((
				Experiment.objects.get(id=t_id),
				self.makeTreatmentsMapping(request, t_id),
				self.makeObservationsMapping(request, t_id)
			))


	def makeTreatmentsMapping(self, request, dataset_id):

		# Finding unique names
		t_experiment = Experiment.objects.get(id=dataset_id)
		t_conditions = Condition.objects.filter(experiment=t_experiment)

		speciesTreatments = []
		for t_condition in t_conditions:
			t_data = Treatment.objects.filter(condition=t_condition)
			speciesTreatments += [str(t_datapoint.species) for t_datapoint in t_data]

		speciesTreatments = list(set(speciesTreatments))

		speciesMapping = []
		for t_species in speciesTreatments:
			if self.view.model.listOfSpecies.containsName(t_species):
				speciesMapping.append((t_species,
						self.view.model.listOfSpecies.getByName(t_species).getSbmlId(),
						self.view.model.listOfSpecies.names().index(t_species),
						self.view.model.listOfSpecies.getByName(t_species).getName(),
						False))

			else:
				speciesMapping.append((t_species, None, -1, None, False))

		return speciesMapping



	def makeObservationsMapping(self, request, dataset_id):

		# Finding unique names
		t_experiment = Experiment.objects.get(id=dataset_id)
		t_conditions = Condition.objects.filter(experiment=t_experiment)

		speciesObservations = []
		for t_condition in t_conditions:
			t_data = Observation.objects.filter(condition=t_condition)
			speciesObservations += [str(t_datapoint.species) for t_datapoint in t_data]

		speciesObservations = list(set(speciesObservations))

		speciesMapping = []
		for t_species in speciesObservations:
			if self.view.model.listOfSpecies.containsName(t_species):
				speciesMapping.append((t_species,
						self.view.model.listOfSpecies.getByName(t_species).getSbmlId(),
						self.view.model.listOfSpecies.names().index(t_species),
						self.view.model.listOfSpecies.getByName(t_species).getName()))

			else:
				speciesMapping.append((t_species, None, -1, None))

		return speciesMapping


	def loadParameters(self, request):

		self.selectedParameters = []

		if "parameter_0_active" not in request.POST:

			# Default parameters
			for parameter in self.view.model.listOfParameters.values():

				self.selectedParameters.append(
					(False, parameter.getNameOrSbmlId(),
						parameter.getValue(),
						parameter.getValue()*1e-4,
						parameter.getValue()*1e4))


			for reaction in self.view.model.listOfReactions.values():
				for parameter in reaction.listOfLocalParameters.values():

					self.selectedParameters.append(
						(False, parameter.getNameOfSbmlId(),
							parameter.getValue(),
							parameter.getValue()*1e-4,
							parameter.getValue()*1e4))


		else:

			i_parameter = 0
			while ("parameter_%d_active" % i_parameter) in request.POST:

				self.selectedParameters.append(
					(i_parameter,
					int(request.POST["parameter_%d_active" % i_parameter]) == 1,
					float(request.POST["parameter_%d_value" % i_parameter]),
					float(request.POST["parameter_%d_min" % i_parameter]),
					float(request.POST["parameter_%d_max" % i_parameter]),
					))

				i_parameter += 1


	def get_user_optimizations_path(self):
		return '{0}/optimizations/{1}/{2}'.format(settings.MEDIA_ROOT,self.project.id, instance.optimization_id)


	def buildExperiments(self, request, interpolate=False):

		list_of_experiments = []

		for i, (experiment, _, _) in enumerate(self.selectedDataSets):

			conditions = Condition.objects.filter(experiment=experiment)
			speciesTreatments = []
			speciesObservations = []
			for t_condition in conditions:
				t_data = Treatment.objects.filter(condition=t_condition).order_by('time')
				speciesTreatments += [str(t_datapoint.species) for t_datapoint in t_data]
				t_data = Observation.objects.filter(condition=t_condition).order_by('time')
				speciesObservations += [str(t_datapoint.species) for t_datapoint in t_data]

			speciesTreatments = list(set(speciesTreatments))
			speciesObservations = list(set(speciesObservations))


			mapping_treatment = {}
			mapping_treatment_interpolation = {}
			i_treatment = 0

			while ("mapping_treatment_%d_%d" % (i, i_treatment)) in request.POST:
				mapping_treatment.update({speciesTreatments[i_treatment]: str(request.POST["mapping_treatment_%d_%d" % (i, i_treatment)])})
				mapping_treatment_interpolation.update({speciesTreatments[i_treatment]: bool(request.POST["mapping_treatment_%d_%d_interpolation" % (i, i_treatment)])})
				i_treatment += 1


			mapping_observation = {}
			i_observation = 0

			while ("mapping_observation_%d_%d" % (i, i_observation)) in request.POST:
				mapping_observation.update({speciesObservations[i_observation]: str(request.POST["mapping_observation_%d_%d" % (i, i_observation)])})
				i_observation += 1


			t_experiment = SigNetSimExperiment()

			for ii, condition in enumerate(conditions):
				# print "> Condition %d" % ii
				observed_data = Observation.objects.filter(condition=condition).order_by('time')
				list_of_experimental_data = ListOfExperimentalData()
				for data in observed_data:
					t_experimental_data = ExperimentalData()
					t_experimental_data.readDB(
							str(data.species), data.time, data.value, data.stddev,
							data.steady_state, data.min_steady_state,
							data.max_steady_state)

					list_of_experimental_data.add(t_experimental_data)

				if interpolate:
					list_of_experimental_data.interpolate()

				input_data = Treatment.objects.filter(condition=condition).order_by('time')

				list_of_input_data = ListOfExperimentalData()
				for iii, data in enumerate(input_data):
					t_experimental_data = ExperimentalData()
					t_experimental_data.readDB(
							str(data.species), data.time, data.value)
					list_of_input_data.add(t_experimental_data)

				if interpolate:
					list_of_input_data.interpolate()

				t_condition = ExperimentalCondition()
				t_condition.read(list_of_input_data, list_of_experimental_data)
				t_condition.name = condition.name
				t_experiment.addCondition(t_condition)

			t_experiment.name = experiment.name
			list_of_experiments.append(t_experiment)


		return list_of_experiments
