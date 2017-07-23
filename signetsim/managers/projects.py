#!/usr/bin/env python
""" users.py


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
from os.path import isdir, isfile, join, splitext, basename
from os import remove
from shutil import rmtree
from signetsim.models import SbmlModel, Experiment, Optimization, SEDMLSimulation, ContinuationComputation, CombineArchiveModel

from signetsim.managers.models import deleteModel, copyModel
from signetsim.managers.data import deleteExperiment, copyExperiment, buildExperiment
from signetsim.managers.simulations import deleteSimulation, copySimulation
from signetsim.managers.optimizations import deleteOptimization
from django.conf import settings
from django.core.files import File

from libsignetsim.combine.CombineArchive import CombineArchive
from libsignetsim.combine.CombineException import CombineException
from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.sedml.SedmlDocument import SedmlDocument
from libsignetsim.model.ModelException import ModelException
from libsignetsim.settings.Settings import Settings


def deleteProject(project):

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
	deleteProjectArchives(project)

	# Deleting folder
	if isdir(join(settings.MEDIA_ROOT, str(project.folder))):
		rmtree(join(settings.MEDIA_ROOT, str(project.folder)))

	project.delete()


def deleteProjectEquilibriumCurve(project):
	for cont in ContinuationComputation.objects.filter(project=project):
		cont.delete()

def deleteProjectArchives(project):
	for archive in CombineArchiveModel.objects.filter(project=project):
		filename = join(settings.MEDIA_ROOT, str(archive.archive_file))
		if isfile(filename):
			remove(filename)
		archive.delete()


def copyProject(project, new_project):
	new_project.save()

	# Copying models
	for model in SbmlModel.objects.filter(project=project):
		copyModel(model, new_project)

	# Copying data
	for experiment in Experiment.objects.filter(project=project):
		copyExperiment(experiment, new_project)

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

		for sbml_file in new_combine_archive.getAllSbmls():
			t_file = File(open(sbml_file, 'r'))

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
#

			for sedml_filename in new_combine_archive.getAllSedmls():
				sedml_archive = SEDMLSimulation(project=new_folder, sedml_file=File(open(sedml_filename, 'r')))
				sedml_archive.name = basename(sedml_filename).split('.')[0]
				sedml_archive.save()

				# Now everything is in the same folder
				sedml_doc = SedmlDocument()
				sedml_doc.readSedmlFromFile(join(settings.MEDIA_ROOT, str(sedml_archive.sedml_file)))
				sedml_doc.listOfModels.removePaths()

				sbml_files = sedml_doc.listOfModels.makeLocalSources()

				for sbml_file in sbml_files:

					if len(SbmlModel.objects.filter(project=new_folder, sbml_file=join(join(str(new_folder.folder), "models"), basename(sbml_file)))) == 0:

						t_file = File(open(sbml_file, 'r'))
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

	except CombineException as e:
		print e.message

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

	archive = None
	if len(CombineArchiveModel.objects.filter(project=project)) == 0:
		archive = CombineArchiveModel(project=project, archive_file=File(open(filename, 'r')))
		archive.name = project.name
		archive.save()
	else:
		archive = CombineArchiveModel.objects.get(project=project)
		t_filename = join(settings.MEDIA_ROOT, str(archive.archive_file))
		if isfile(t_filename) and filename != t_filename:
			remove(t_filename)
			archive.archive_file = File(open(filename))
			archive.save()

	if archive is not None:
		return join(settings.MEDIA_ROOT, str(archive.archive_file))
