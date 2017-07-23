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
from os.path import isdir, join
from shutil import rmtree
from django.conf import settings

def deleteOptimization(optimization):

	subdirectory = "optimization_%s" % optimization.optimization_id
	directory = join(settings.MEDIA_ROOT, optimization.project.folder, "optimizations", subdirectory)
	if isdir(directory):
		rmtree(directory)
	optimization.delete()
