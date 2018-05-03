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

""" models.py

	This file ...

"""

from os.path import isfile, join, dirname
from os import remove
from signetsim.models import SbmlModel, new_model_filename
from libsignetsim import SbmlDocument
from django.core.files import File
from django.conf import settings

def deleteModel(model):

	filename = join(settings.MEDIA_ROOT, str(model.sbml_file))
	if isfile(filename):
		remove(filename)
	model.delete()

def copyModel(model, new_project):

	t_file = File(open(join(settings.MEDIA_ROOT, str(model.sbml_file)), 'rb'))

	new_model = SbmlModel(project=new_project, name=model.name,	sbml_file=t_file)
	new_model.save()

def copyModelHierarchy(model_filename):

	doc = SbmlDocument()
	doc.readSbmlFromFile(model_filename)
	path = dirname(model_filename)
	master_filename = new_model_filename()

	if doc.useCompPackage:
		deps = doc.getExternalDocumentDependencies()
		new_deps = {}
		for dependency in deps:
			new_deps.update({dependency: copyModelHierarchy(join(path, dependency))})

		doc.renameExternalDocumentDependencies(new_deps)

	doc.writeSbmlToFile(join(path, master_filename))
	return master_filename

def deleteModelHierarchy(model_filename):

	doc = SbmlDocument()
	doc.readSbmlFromFile(model_filename)
	path = dirname(model_filename)

	if doc.useCompPackage:
		for dependency in doc.getExternalDocumentDependencies():
			deleteModelHierarchy(join(path, dependency))

	remove(model_filename)

def getModelHierarchy(model_filename):

	doc = SbmlDocument()
	doc.readSbmlFromFile(model_filename)
	path = dirname(model_filename)
	deps = []
	if doc.useCompPackage:
		for dependency in doc.getExternalDocumentDependencies():
			deps.append(dependency)
			deps += getModelHierarchy(join(path, dependency))

	return deps