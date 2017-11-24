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

""" simulations.py

	This file ...

"""

from os.path import isfile, join, relpath
from os import remove
from signetsim.models import SEDMLSimulation, SbmlModel
from signetsim.managers.models import deleteModelHierarchy
from django.core.files import File
from django.conf import settings

def deleteSimulation(simulation):

	filename = join(settings.MEDIA_ROOT, str(simulation.sedml_file))
	if isfile(filename):
		remove(filename)

	sbml_filename = join(settings.MEDIA_ROOT, str(simulation.sbml_file))

	# If it exists, but is not references outside of the simulation
	if isfile(sbml_filename) and not SbmlModel.objects.filter(sbml_file=relpath(sbml_filename, settings.MEDIA_ROOT)).exists():
		deleteModelHierarchy(sbml_filename)

	simulation.delete()

def copySimulation(simulation, new_project):

	t_file = File(open(join(settings.MEDIA_ROOT, str(simulation.sedml_file))))
	new_simulation = SEDMLSimulation(project=new_project, name=simulation.name, sedml_file=t_file)
	new_simulation.save()
