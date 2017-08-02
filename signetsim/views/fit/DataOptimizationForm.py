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

from django.conf import settings

from signetsim.models import Experiment, Condition
from signetsim.models import Observation, Treatment
from signetsim.views.HasErrorMessages import HasErrorMessages
from libsignetsim.data.Experiment import Experiment as SigNetSimExperiment
from libsignetsim.data.ExperimentalCondition import ExperimentalCondition
from libsignetsim.data.ListOfExperimentalData import ListOfExperimentalData
from libsignetsim.data.ExperimentalData import ExperimentalData

from libsignetsim.settings.Settings import Settings

class DataOptimizationForm(HasErrorMessages):

	def __init__(self, view, **kwargs):

		HasErrorMessages.__init__(self)
		self.view = view

		self.selectedDataSets = None
		self.selectedDataSetsIds = None

		self.speciesMapping = None
		self.selectedParameters = None

		self.nbCores = 2
		self.plsaLambda = Settings.defaultPlsaLambda
		self.plsaCriterion = Settings.defaultPlsaCriterion
		self.plsaInitialTemperature = Settings.defaultPlsaInitialTemperature
		self.plsaInitialMoves = Settings.defaultPlsaInitialMoves
		self.scoreNegativePenalty = Settings.defaultScoreNegativePenalty

	def readSettings(self, request):
		self.nbCores = self.readInt(request, 'nb_cores', "the number of cores")
		self.plsaLambda = self.readFloat(request, 'lambda', "the lambda setting")
		self.plsaCriterion = self.readFloat(request, 'precision', "the precision setting")
		self.plsaInitialTemperature = self.readFloat(request, 'initial_temperature', "the initial temperature setting")
		self.plsaInitialMoves = self.readFloat(request, 'initial_moves', "the initial moves setting")
		self.scoreNegativePenalty = self.readFloat(request, 'negative_penalty', "the negative penalty setting")

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
				None,
				None
				# self.makeTreatmentsMapping(request, t_id),
				# self.makeObservationsMapping(request, t_id)
			))

	#
	# def makeTreatmentsMapping(self, request, dataset_id):
	#
	# 	# Finding unique names
	# 	t_experiment = Experiment.objects.get(id=dataset_id)
	# 	t_conditions = Condition.objects.filter(experiment=t_experiment)
	#
	# 	speciesTreatments = []
	# 	for t_condition in t_conditions:
	# 		t_data = Treatment.objects.filter(condition=t_condition)
	# 		speciesTreatments += [str(t_datapoint.species) for t_datapoint in t_data]
	#
	# 	speciesTreatments = list(set(speciesTreatments))
	#
	# 	speciesMapping = []
	# 	for t_species in speciesTreatments:
	# 		if self.view.model.listOfSpecies.containsName(t_species):
	# 			speciesMapping.append((t_species,
	# 					self.view.model.listOfSpecies.getByName(t_species).getSbmlId(),
	# 					self.view.model.listOfSpecies.names().index(t_species),
	# 					self.view.model.listOfSpecies.getByName(t_species).getName(),
	# 					False))
	#
	# 		else:
	# 			speciesMapping.append((t_species, None, -1, None, False))
	#
	# 	return speciesMapping
	#
	#
	#
	# def makeObservationsMapping(self, request, dataset_id):
	#
	# 	# Finding unique names
	# 	t_experiment = Experiment.objects.get(id=dataset_id)
	# 	t_conditions = Condition.objects.filter(experiment=t_experiment)
	#
	# 	speciesObservations = []
	# 	for t_condition in t_conditions:
	# 		t_data = Observation.objects.filter(condition=t_condition)
	# 		speciesObservations += [str(t_datapoint.species) for t_datapoint in t_data]
	#
	# 	speciesObservations = list(set(speciesObservations))
	#
	# 	speciesMapping = []
	# 	for t_species in speciesObservations:
	# 		if self.view.model.listOfSpecies.containsName(t_species):
	# 			speciesMapping.append((t_species,
	# 					self.view.model.listOfSpecies.getByName(t_species).getSbmlId(),
	# 					self.view.model.listOfSpecies.names().index(t_species),
	# 					self.view.model.listOfSpecies.getByName(t_species).getName()))
	#
	# 		else:
	# 			speciesMapping.append((t_species, None, -1, None))
	#
	# 	return speciesMapping
	#

	def loadParameters(self, request):
		print request.POST

		self.selectedParameters = []

		if "parameter_0_id" not in request.POST:

			# Default parameters
			i_parameter = 0
			for parameter in self.view.model.listOfParameters.values():

				self.selectedParameters.append(
					(
						i_parameter, False,
						parameter.getNameOrSbmlId(),
						parameter.getValue(),
						parameter.getValue()*1e-4,
						parameter.getValue()*1e4))

				i_parameter += 1

			for reaction in self.view.model.listOfReactions.values():
				for parameter in reaction.listOfLocalParameters.values():

					self.selectedParameters.append(
						(
							i_parameter, False,
							parameter.getNameOfSbmlId(),
							parameter.getValue(),
							parameter.getValue()*1e-4,
							parameter.getValue()*1e4))


		else:
			i_parameter = 0
			while ("parameter_%d_id" % i_parameter) in request.POST:

				t_active = self.readOnOff(
					request, 'parameter_%d_active' % i_parameter,
					"the status of the parameter #%d" % i_parameter
				)
				print t_active
				t_name = self.readString(
					request, 'parameter_%d_name' % i_parameter,
					"the name of the parameter #%d" % i_parameter
				)

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
				self.selectedParameters.append(
					(i_parameter, t_active, t_name, t_value, t_min, t_max)
				)

				i_parameter += 1

		# print self.selectedParameters

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
