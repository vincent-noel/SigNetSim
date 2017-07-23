#!/usr/bin/env python
#
# Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

""" users.py


	This file ...


"""

from signetsim.models import Experiment, Condition, Observation, Treatment
from libsignetsim.data.Experiment import Experiment as SigNetSimExperiment


def deleteExperiment(experiment):

	for condition in Condition.objects.filter(experiment=experiment):
		for observation in Observation.objects.filter(condition=condition):
			observation.delete()
		for treatment in Treatment.objects.filter(condition=condition):
			treatment.delete()
		condition.delete()
	experiment.delete()

def copyExperiment(experiment, new_project):


	new_experiment = Experiment(project=new_project,
									name=str(experiment.name),
									notes=str(experiment.notes))
	new_experiment.save()
	t_conditions = Condition.objects.filter(experiment=experiment)
	for condition in t_conditions:
		new_condition = Condition(experiment=new_experiment,
									name=str(condition.name),
									notes=str(condition.notes))
		new_condition.save()

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

		new_condition.save()
	new_experiment.save()


def buildExperiment(experiment):

	conditions = Condition.objects.filter(experiment=experiment)
	t_experiment = SigNetSimExperiment(experiment.name)

	for condition in conditions:
		t_condition = t_experiment.createCondition(str(condition.name))
		observed_data = Observation.objects.filter(condition=condition)

		for data in observed_data:
			t_condition.addObservation(data.time, data.species, data.value)

		input_data = Treatment.objects.filter(condition=condition)

		for data in input_data:
			t_condition.addInitialCondition(data.time, data.species, data.value)

	return t_experiment
