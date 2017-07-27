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
from os.path import isfile, join
from os import remove
from signetsim.models import SbmlModel
from django.core.files import File
from django.conf import settings

def deleteModel(model):

	filename = join(settings.MEDIA_ROOT, str(model.sbml_file))
	if isfile(filename):
		remove(filename)
	model.delete()

def copyModel(model, new_project):

	t_file = File(open(join(settings.MEDIA_ROOT, str(model.sbml_file))))

	new_model = SbmlModel(project=new_project, name=model.name,
							sbml_file=t_file)
	new_model.save()