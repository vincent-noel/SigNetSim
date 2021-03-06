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

""" projects.py

	This file ...

"""

from django.conf import settings
from django.core.files import File

from signetsim.models import SbmlModel, Experiment, Optimization, SEDMLSimulation, Continuation, ModelsDependency
from signetsim.managers.models import deleteModel, copyModel, getDetailedModelDependencies
from signetsim.managers.data import deleteExperiment, copyExperiment, buildExperiment, importExperiment
from signetsim.managers.simulations import deleteSimulation, copySimulation
from signetsim.managers.optimizations import deleteOptimization

from libsignetsim import CombineArchive, CombineException, SbmlDocument, SedmlDocument, ModelException, Settings

from os.path import isdir, join, splitext, basename
from shutil import rmtree


def deleteProject(project):

	for modelDependency in ModelsDependency.objects.filter(project=project):
		modelDependency.delete()

	# Deleting models
	for model in SbmlModel.objects.filter(project=project):
		deleteModel(model)

	# Deleting data
	for experiment in Experiment.objects.filter(project=project):
		deleteExperiment(experiment)

	# Deleting simulations
	for simulation in SEDMLSimulation.objects.filter(project=project):
		deleteSimulation(simulation)

	# Deleting optimization
	for optim in Optimization.objects.filter(project=project):
		deleteOptimization(optim)




	deleteProjectEquilibriumCurve(project)
	# deleteProjectArchives(project)

	# Deleting folder
	if isdir(join(settings.MEDIA_ROOT, str(project.folder))):
		rmtree(join(settings.MEDIA_ROOT, str(project.folder)))

	project.delete()


def deleteProjectEquilibriumCurve(project):
	for cont in Continuation.objects.filter(project=project):
		cont.delete()

# def deleteProjectArchives(project):
# 	for archive in CombineArchiveModel.objects.filter(project=project):
# 		filename = join(settings.MEDIA_ROOT, str(archive.archive_file))
# 		if isfile(filename):
# 			remove(filename)
# 		archive.delete()


def copyProject(project, new_project):
	new_project.save()

	# Copying models
	for model in SbmlModel.objects.filter(project=project):
		copyModel(model, new_project)

	# Copying data
	for experiment in Experiment.objects.filter(project=project):
		new_experiment = Experiment(project=new_project,
									name=str(experiment.name),
									notes=str(experiment.notes))
		new_experiment.save()
		copyExperiment(experiment, new_experiment)

	# Copying simulations
	for simulation in SEDMLSimulation.objects.filter(project=project):
		copySimulation(simulation, new_project)

	new_project.save()

def importProject(new_folder, filename):

	new_combine_archive = CombineArchive()
	new_folder.name = basename(filename).split('.')[0]
	new_folder.save()

	try:
		new_combine_archive.readArchive(filename)

		deps = []
		for sbml_file in new_combine_archive.getAllSbmls():
			t_file = File(open(sbml_file, 'rb'))

			sbml_model = SbmlModel(project=new_folder, sbml_file=t_file)
			sbml_model.save()

			try:
				doc = SbmlDocument()

				doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(sbml_model.sbml_file)))

				dependencies = getDetailedModelDependencies(doc)
				if len(dependencies) > 0:
					deps.append((sbml_model, dependencies))

				sbml_model.name = doc.model.getName()
				sbml_model.save()
			except ModelException:
				name = splitext(str(sbml_model.sbml_file))[0]
				sbml_model.name = name
				sbml_model.save()

		for model, submodels in deps:

			for submodel_filename, submodel_ref in submodels:
				submodel_filename = join(new_folder.folder, "models", submodel_filename)
				submodel = SbmlModel.objects.get(sbml_file=submodel_filename)
				new_dependency = ModelsDependency(project=new_folder, model=model, submodel=submodel, submodel_ref=submodel_ref)
				new_dependency.save()

		for sedml_filename in new_combine_archive.getAllSedmls():

			sedml_archive = SEDMLSimulation(project=new_folder, sedml_file=File(open(sedml_filename, 'rb')))
			sedml_archive.name = basename(sedml_filename).split('.')[0]
			sedml_archive.save()

			# Now everything is in the same folder
			sedml_doc = SedmlDocument()
			sedml_doc.readSedmlFromFile(join(settings.MEDIA_ROOT, str(sedml_archive.sedml_file)))
			sedml_doc.listOfModels.removePaths()
			sbml_files = sedml_doc.listOfModels.makeLocalSources()

			for sbml_file in sbml_files:

				if len(SbmlModel.objects.filter(project=new_folder, sbml_file=join(join(str(new_folder.folder), "models"), basename(sbml_file)))) == 0:

					t_file = File(open(sbml_file, 'rb'))
					sbml_model = SbmlModel(project=new_folder, sbml_file=t_file)
					sbml_model.save()
					try:
						doc = SbmlDocument()

						doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(sbml_model.sbml_file)))

						sbml_model.name = doc.model.getName()
						sbml_model.save()
					except ModelException:
						name = splitext(str(sbml_model.sbml_file))[0]
						sbml_model.name = name
						sbml_model.save()

			sedml_doc.writeSedmlToFile(join(settings.MEDIA_ROOT, str(sedml_archive.sedml_file)))


		for numl_file in new_combine_archive.getAllNumls():
			new_experiment = Experiment(project=new_folder)
			new_experiment.save()
			importExperiment(new_experiment, numl_file)

	except CombineException as e:
		print(e.message)

def exportProject(project):

	combine_archive = CombineArchive()
	for sbml_model in SbmlModel.objects.filter(project=project):
		combine_archive.addFile(join(settings.MEDIA_ROOT, str(sbml_model.sbml_file)))

	for sedml_model in SEDMLSimulation.objects.filter(project=project):
		combine_archive.addFile(join(settings.MEDIA_ROOT, str(sedml_model.sedml_file)))

	for i, experiment in enumerate(Experiment.objects.filter(project=project)):
		t_experiment = buildExperiment(experiment)
		t_experiment.writeNuMLToFile(join(Settings.tempDirectory, "experiment_%d.xml" % i))
		combine_archive.addFile(join(Settings.tempDirectory, "experiment_%d.xml" % i))

	filename = ''.join(e for e in project.name if e.isalnum()) + ".omex"
	filename = join(Settings.tempDirectory, filename)
	combine_archive.writeArchive(filename)
	return filename

