#!/usr/bin/env python
""" DataOptimizationView0.py


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
from signetsim.models import SbmlModel, Optimization
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
import pickle

class DataOptimizationView0(TemplateView, HasWorkingModel):

	template_name = 'fit/data.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)

		self.listOfDataSets = None

		self.selectedDataSets = None
		self.selectedDataSetsIds = None

		self.listOfSpecies = None
		self.speciesMapping = None
		self.selectedParameters = None


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)

		kwargs['experimental_data_sets'] = self.listOfDataSets
		kwargs['selected_datasets'] = self.selectedDataSets
		kwargs['selected_datasets_ids'] = self.selectedDataSetsIds

		kwargs['list_of_species'] = self.listOfSpecies
		kwargs['selected_parameters'] = self.selectedParameters

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
				self.addDataset(request)

			elif request.POST['action'] == "remove_dataset":
				self.removeDataset(request)

			elif request.POST['action'] == "create":
				self.runOptimization(request)



		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)

		if self.isModelLoaded():
			self.loadSpecies()
			self.loadDataSets(request)
			self.loadParameters(request)


	def runOptimization(self, request):

		self.readSelectedDataset(request)
		self.loadMapping(request)

		experiments = self.buildExperiments(request)


		t_optimization = ModelVsTimeseriesOptimization(
							workingModel = self.getModelInstance(),
							list_of_experiments = experiments,
							mapping=self.speciesMapping,
							parameters_to_fit=self.selectedParameters)

		if not os.path.isdir(os.path.join(settings.MEDIA_ROOT, str(self.project.folder), "optimizations")):
			os.mkdir(os.path.join(settings.MEDIA_ROOT, str(self.project.folder), "optimizations"))
		t_optimization.setTempDirectory(os.path.join(settings.MEDIA_ROOT, str(self.project.folder), "optimizations"))
		nb_procs = 4

		print "calling from the view"
		ModelVsTimeseriesOptimization.writeOptimizationFiles(t_optimization, nb_procs=nb_procs)
		print "view is done"
		t = threading.Thread(group=None,
								target=t_optimization.runOptimization,
								args=(nb_procs, None, None, ))

		t.setDaemon(True)
		t.start()

		new_optimization = Optimization(project=self.project,
								model=SbmlModel.objects.get(id=self.model_id),
								optimization_id=t_optimization.optimizationId)
		new_optimization.save()


	def removeDataset(self, request):

		self.readSelectedDataset(request)
		dataset_id = int(request.POST['dataset_id'])
		self.selectedDataSetsIds.remove(dataset_id)
		self.loadMapping(request)


	def addDataset(self, request):

		self.readSelectedDataset(request)

		dataset_id = self.listOfDataSets[int(
								request.POST['dataset_id'])].id

		self.selectedDataSetsIds.append(dataset_id)
		self.selectedDataSetsIds = list(set(self.selectedDataSetsIds))

		self.loadMapping(request)


	def loadMapping(self, request):
		# print request

		# Building mappings
		self.speciesMapping = []
		for t_dataset_id in self.selectedDataSetsIds:
			self.speciesMapping.append(self.makeMapping(request,
													t_dataset_id))

		self.selectedDataSets = []
		for i, t_id in enumerate(self.selectedDataSetsIds):
			self.selectedDataSets.append((
				Experiment.objects.get(id=t_id),
				self.speciesMapping[i]))


	def makeMapping(self, request, dataset_id):

		# Finding unique names
		t_experiment = Experiment.objects.get(id=dataset_id)
		t_conditions = Condition.objects.filter(experiment=t_experiment)

		speciesData = []
		for t_condition in t_conditions:

			t_data = Observation.objects.filter(condition=t_condition)

			speciesData += [str(t_datapoint.species) for t_datapoint in t_data]

			t_data = Treatment.objects.filter(condition=t_condition)

			speciesData += [str(t_datapoint.species) for t_datapoint in t_data]

		speciesData = list(set(speciesData))

		speciesMapping = []
		for t_species in speciesData:
			if self.getModelInstance().listOfSpecies.containsName(t_species):
				speciesMapping.append((t_species,
						self.getModelInstance().listOfSpecies.getByName(t_species).getSbmlId(),
						self.getModelInstance().listOfSpecies.getByName(t_species).getName(), False))

			else:
				speciesMapping.append((t_species, None, None, False))

		return speciesMapping


	def readSelectedDataset(self, request):

		self.selectedDataSetsIds = []
		i_dataset_selected = 0

		while ("dataset_%d" % i_dataset_selected) in request.POST:
			self.selectedDataSetsIds.append(
				int(request.POST["dataset_%d" % i_dataset_selected]))

			i_dataset_selected += 1


	def loadSpecies(self):
		self.listOfSpecies = self.getModelInstance().listOfSpecies.values()


	def loadDataSets(self, request):

		self.listOfDataSets = Experiment.objects.filter(project=self.project)
		# conditions_data_sets = Condition.objects.filter(user=request.user)


	def loadParameters(self, request):

		self.selectedParameters = []

		if "parameter_0_active" not in request.POST:

			# Default parameters
			for parameter in self.getModelInstance().listOfParameters.values():

				self.selectedParameters.append(
					(None, parameter.objId, True, parameter.getNameOrSbmlId(),
						parameter.getValue(),
						parameter.getValue()*1e-4,
						parameter.getValue()*1e4))


			for reaction in self.getModelInstance().listOfReactions.values():
				for parameter in reaction.listOfLocalParameters.values():

					self.selectedParameters.append(
						(reaction.objId ,parameter.objId,
							True, parameter.getNameOrSbmlId(),
							parameter.getValue(),
							parameter.getValue()*1e-4,
							parameter.getValue()*1e4))


		else:

			i_parameter = 0
			while ("parameter_%d_active" % i_parameter) in request.POST:

				if str(request.POST['parameter_%d_rid' % i_parameter]) == "None":
					parameter_rid = None
				else:
					parameter_rid = int(request.POST['parameter_%d_rid' % i_parameter])

				self.selectedParameters.append(
					(parameter_rid, int(request.POST['parameter_%d_id' % i_parameter]),
					(int(request.POST["parameter_%d_active" % i_parameter]) == 1),
					str(request.POST["parameter_%d_name" % i_parameter]),
					float(request.POST["parameter_%d_value" % i_parameter]),
					float(request.POST["parameter_%d_min" % i_parameter]),
					float(request.POST["parameter_%d_max" % i_parameter]),
					))
				i_parameter += 1

	def get_user_optimizations_path(self):
		# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
		# return os.path.join(settings.MEDIA_ROOT, self.project.id,
		return '{0}/optimizations/{1}/{2}'.format(settings.MEDIA_ROOT,self.project.folder, instance.optimization_id)


	def buildExperiments(self, request, interpolate=True):

		list_of_experiments = {}
		for i, (experiment, _) in enumerate(self.selectedDataSets):

			t_experiment = SigNetSimExperiment()
			conditions = Condition.objects.filter(experiment=experiment)

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

				#list_of_experimental_data.interpolate()

				input_data = Treatment.objects.filter(condition=condition).order_by('time')

				list_of_input_data = ListOfExperimentalData()
				for iii, data in enumerate(input_data):
					t_experimental_data = ExperimentalData()
					t_experimental_data.readDB(
							str(data.species), data.time, data.value)
					list_of_input_data.add(t_experimental_data)

				#list_of_input_data.interpolate()


				t_condition = ExperimentalCondition()
				t_condition.read(list_of_input_data, list_of_experimental_data)
				t_condition.name = condition.name
				t_experiment.addCondition(t_condition)

			t_experiment.name = experiment.name
			list_of_experiments.update({len(list_of_experiments): t_experiment})


		return list_of_experiments
