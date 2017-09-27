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

""" optimizations.py

	This file ...

"""

from os.path import isdir, join
from shutil import rmtree
from django.conf import settings

def deleteOptimization(optimization):

	subdirectory = "optimization_%s" % optimization.optimization_id
	directory = join(settings.MEDIA_ROOT, optimization.project.folder, "optimizations", subdirectory)
	if isdir(directory):
		rmtree(directory)
	optimization.delete()
