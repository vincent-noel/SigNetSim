#!/usr/bin/env python
""" models.py


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

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits
from os.path import dirname, basename, join

def new_model_filename():
	rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	return "model{0}.xml".format(rand_string)

def new_sedml_filename():
	rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	return "simulation{0}.xml".format(rand_string)

def new_project_folder():
	rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	while os.path.isdir(os.path.join(settings.MEDIA_ROOT, rand_string)):
		rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	return rand_string


def model_filename(instance, filename):

	path = dirname(filename)
	filename = basename(filename)
	full_path = join(join(path, "models"), str(instance.project.folder))
	full_filename = join(full_path, filename)

	# full_filename = '{0}/models/{1}'.format(instance.project.folder, filename)
	while os.path.isfile(full_filename):
		full_filename = join(full_path, new_model_filename())
	return full_filename

def sedml_filename(instance, filename):
	filename = '{0}/simulations/{1}'.format(instance.project.folder, new_sedml_filename())
	while os.path.isfile(filename):
		filename = '{0}/simulations/{1}'.format(instance.project.folder, new_sedml_filename())
	return filename


class User(AbstractUser):
	"""
	Custom user class.
	"""
	fullname = models.CharField(max_length=255, null=True)
	max_cores = models.IntegerField(null=2)


class Project(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=255, null=True)
	folder = models.CharField(max_length=255, default=new_project_folder)
	PUBLIC = 'PU'
	PRIVATE = 'PR'

	ACCESS_CHOICES = (
		(PUBLIC, 'Public'),
		(PRIVATE, 'Private'),
	)

	access = models.CharField(max_length=2,
									  choices=ACCESS_CHOICES,
									  default=PRIVATE)



class SbmlModel(models.Model):
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=255, null=True)
	sbml_file = models.FileField(upload_to=model_filename)


class SEDMLSimulation(models.Model):
	sbml_model = models.ForeignKey(SbmlModel)
	name = models.CharField(max_length=255, null=True)
	sedml_file = models.FileField(upload_to=sedml_filename)


# class FittedSbmlModel(models.Model):
#
#     project = models.ForeignKey(Project)
#     optimization_id = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     sbml_file = models.FileField(upload_to=fitted_model_filename)


class Optimization(models.Model):
	project = models.ForeignKey(Project)
	model = models.ForeignKey(SbmlModel)
	optimization_id = models.CharField(max_length=255)


class ContinuationComputation(models.Model):
	project = models.ForeignKey(Project)
	model = models.ForeignKey(SbmlModel)

	variable = models.CharField(max_length=255, default="")
	parameter = models.CharField(max_length=255, default="")

	figure = models.CharField(max_length=10240, default="")

	BUSY = 'BU'
	ENDED = 'EN'
	ERROR = 'ER'

	STATUSES = (
		(BUSY, 'Busy'),
		(ENDED, 'Ended'),
		(ERROR, 'Error')
	)

	status = models.CharField(max_length=2,
									  choices=STATUSES,
									  default=BUSY)


#######################################################################################
# Experimental data v2
#######################################################################################
class Experiment(models.Model):
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=255)
	notes = models.CharField(max_length=2048, null=True)

class Condition(models.Model):
	experiment = models.ForeignKey(Experiment)
	name = models.CharField(max_length=255)
	notes = models.CharField(max_length=2048, null=True)


class Observation(models.Model):
	condition = models.ForeignKey(Condition)
	species = models.CharField(max_length=255)

	time = models.FloatField()
	value = models.FloatField()
	stddev = models.FloatField()
	steady_state = models.BooleanField()
	min_steady_state = models.FloatField(null = True)
	max_steady_state = models.FloatField(null = True)

	def create(cls, species, time, value, stddev, steady_state, min_steady_state, max_steady_state):
		data_point = cls(species=species, time=time, value=value, stddev=stddev,
							steady_state=steady_state,
							min_steady_state=min_steady_state,
							max_steady_state=max_steady_state)
		return data_point

class Treatment(models.Model):
	condition = models.ForeignKey(Condition)
	species = models.CharField(max_length=255)

	time = models.FloatField()
	value = models.FloatField()

	def create(cls, species, time, value):
		data_point = cls(species=species, time=time, value=value)
		return data_point
