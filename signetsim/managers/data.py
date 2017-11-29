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

""" data.py

	This file ...

"""

from signetsim.models import Experiment, Condition, Observation, Treatment
from libsignetsim import Experiment as SigNetSimExperiment
from django.conf import settings
from os.path import join

def deleteExperiment(experiment):

	for condition in Condition.objects.filter(experiment=experiment):
		for observation in Observation.objects.filter(condition=condition):
			observation.delete()
		for treatment in Treatment.objects.filter(condition=condition):
			treatment.delete()
		condition.delete()
	experiment.delete()

def copyExperiment(experiment, new_experiment):


	t_conditions = Condition.objects.filter(experiment=experiment)
	for condition in t_conditions:
		new_condition = Condition(experiment=new_experiment)
		new_condition.save()

		copyCondition(condition, new_condition)

	new_experiment.name = experiment.name
	new_experiment.notes = experiment.notes
	new_experiment.save()

def copyCondition(condition, new_condition):

	t_observations = Observation.objects.filter(condition=condition)
	for t_observation in t_observations:
		new_observation = Observation(condition=new_condition,
									  species=t_observation.species,
									  time=t_observation.time,
									  value=t_observation.value,
									  stddev=t_observation.stddev,
									  steady_state=t_observation.steady_state,
									  min_steady_state=t_observation.min_steady_state,
									  max_steady_state=t_observation.max_steady_state)

		new_observation.save()

	t_treatments = Treatment.objects.filter(condition=condition)
	for t_treatment in t_treatments:
		new_treatment = Treatment(condition=new_condition,
								  species=t_treatment.species,
								  time=t_treatment.time,
								  value=t_treatment.value)

		new_treatment.save()

	new_condition.name = condition.name
	new_condition.notes = condition.notes
	new_condition.save()


def exportExperiment(experiment):

	t_experiment = buildExperiment(experiment)
	t_filename = join(settings.MEDIA_ROOT, "experiment.xml")
	t_experiment.writeNuMLToFile(join(settings.MEDIA_ROOT, "experiment.xml"))

	return t_filename


def importExperiment(experiment, filename):

	t_experiment = SigNetSimExperiment()
	t_experiment.readNuMLFromFile(filename)

	experiment.name = t_experiment.name
	experiment.save()

	for t_condition in t_experiment.listOfConditions.values():

		condition = Condition(experiment=experiment, name=t_condition.name)
		condition.save()

		for t_initial_value in t_condition.listOfInitialConditions.values():

			initial_value = Treatment(
				condition=condition,
				species=t_initial_value.name,
				time=t_initial_value.t,
				value=t_initial_value.value
			)
			initial_value.save()

		for t_observation in t_condition.listOfExperimentalData.values():

			observation = Observation(
				condition=condition,
				species=t_observation.name,
				time=t_observation.t,
				value=t_observation.value,
				stddev=t_observation.value_dev,
				steady_state=t_observation.steady_state,
				min_steady_state=t_observation.min_steady_state,
				max_steady_state=t_observation.max_steady_state
			)
			observation.save()


def buildExperiment(experiment):

	conditions = Condition.objects.filter(experiment=experiment)
	t_experiment = SigNetSimExperiment(experiment.name)
	t_experiment.notes = str(experiment.notes)

	for condition in conditions:
		t_condition = t_experiment.createCondition(str(condition.name))
		t_condition.notes = str(condition.notes)
		observed_data = Observation.objects.filter(condition=condition)

		for data in observed_data:
			t_condition.addObservation(data.time, data.species, data.value)

		input_data = Treatment.objects.filter(condition=condition)

		for data in input_data:
			t_condition.addInitialCondition(data.time, data.species, data.value)

	return t_experiment


