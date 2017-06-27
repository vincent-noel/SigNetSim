#!/usr/bin/env python
""" manager.py


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
from os.path import isdir, isfile, join
from os import remove
from shutil import rmtree
from models import (
	SbmlModel, Experiment, Condition, Observation, Treatment, Optimization, User, Project, SEDMLSimulation,
	ContinuationComputation, CombineArchiveModel
)
from django.core.files import File
from django.conf import settings


def	deleteUser(user):

	for project in Project.objects.filter(user=user):
		deleteProject(project)
	user.delete()

def deleteProject(project):

	deleteProjectModels(project)
	deleteProjectData(project)
	deleteProjectOptimizations(project)
	deleteProjectEquilibriumCurve(project)
	deleteProjectArchives(project)
	deleteProjectFolder(project)

	project.delete()

def deleteProjectModels(project):

	for model in SbmlModel.objects.filter(project=project):
		filename = join(settings.MEDIA_ROOT, str(model.sbml_file))
		if isfile(filename):
			remove(filename)
		model.delete()

def deleteProjectData(project):

	for experiment in Experiment.objects.filter(project=project):
		for condition in Condition.objects.filter(experiment=experiment):
			for observation in Observation.objects.filter(condition=condition):
				observation.delete()
			for treatment in Treatment.objects.filter(condition=condition):
				treatment.delete()
			condition.delete()
		experiment.delete()

def deleteProjectOptimizations(project):
	for optim in Optimization.objects.filter(project=project):
		subdirectory = "optimization_%s" % optim.optimization_id
		directory = join(settings.MEDIA_ROOT, project.folder, "optimizations", subdirectory)
		if isdir(directory):
			rmtree(directory)
		optim.delete()

def deleteProjectEquilibriumCurve(project):
	for cont in ContinuationComputation.objects.filter(project=project):
		cont.delete()

def deleteProjectSimulations(project):
	for simulation in SEDMLSimulation.objects.filter(project=project):
		filename = join(settings.MEDIA_ROOT, str(simulation.sedml_file))
		if isfile(filename):
			remove(filename)
		simulation.delete()

def deleteProjectArchives(project):
	for archive in CombineArchiveModel.objects.filter(project=project):
		filename = join(settings.MEDIA_ROOT, str(archive.archive_file))
		if isfile(filename):
			remove(filename)
		archive.delete()

def deleteProjectFolder(project):
	if isdir(join(settings.MEDIA_ROOT, str(project.folder))):
		rmtree(join(settings.MEDIA_ROOT, str(project.folder)))


def copyProject(project, new_project):
	new_project.save()
	copyProjectModels(project, new_project)
	copyProjectExperiments(project, new_project)

	new_project.save()

def copyProjectModels(project, new_project):

	t_models = SbmlModel.objects.filter(project=project)
	for model in t_models:
		t_file = File(open(join(settings.MEDIA_ROOT, str(model.sbml_file))))

		new_model = SbmlModel(project=new_project, name=model.name,
								sbml_file=t_file)
		new_model.save()

def copyProjectExperiments(project, new_project):

	t_experiments = Experiment.objects.filter(project=project)
	for experiment in t_experiments:

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
