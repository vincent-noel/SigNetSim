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

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files import File
from libsignetsim import SbmlDocument
import os
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits, punctuation
from os.path import dirname, basename, join

def new_model_filename():
	rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	return "model{0}.xml".format(rand_string)

def new_sedml_filename():
	rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	return "simulation{0}.xml".format(rand_string)

def new_archive_filename():
	rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	return "archive{0}.omex".format(rand_string)

def new_project_folder():
	rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	while os.path.isdir(os.path.join(settings.MEDIA_ROOT, rand_string)):
		rand_string = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(6))
	return rand_string

def new_secret_key():
	return ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(60))

def archive_filename(instance, filename):

	filename = basename(filename)

	full_path = join(str(instance.project.folder), "models")
	full_filename = join(full_path, filename)

	while os.path.isfile(full_filename):
		full_filename = join(full_path, new_archive_filename())

	return full_filename

def model_filename(instance, filename):

	filename = basename(filename)

	full_path = join(str(instance.project.folder), "models")
	full_filename = join(full_path, filename)

	while os.path.isfile(full_filename):
		full_filename = join(full_path, new_model_filename())

	return full_filename

def sedml_filename(instance, filename):

	filename = basename(filename)

	full_path = join(str(instance.project.folder), "models")
	full_filename = join(full_path, filename)

	while os.path.isfile(full_filename):
		full_filename = join(full_path, new_sedml_filename())

	return full_filename

class User(AbstractUser):
	"""
	Custom user class.
	"""
	organization = models.CharField(max_length=255, null=True)
	used_cores = models.IntegerField(null=False, default=0)
	max_cores = models.IntegerField(null=False, default=2)
	used_cpu_time = models.FloatField(null=False, default=0)
	max_cpu_time = models.IntegerField(null=False, default=1000)

	# this is not needed if small_image is created at set_image
	def save(self, *args, **kwargs):

		if User.objects.filter(id=self.id).exists():
			created = False
		else:
			created = True

		super(User, self).save(*args, **kwargs)

		if created:
			new_project = Project(user=self, name="My first project")
			new_project.save()

			sbml_model_filename = join(settings.MEDIA_ROOT, "init_model.sbml")
			sbml_model = open(sbml_model_filename, 'a')
			sbml_model.close()

			new_model = SbmlModel(project=new_project, name="My first model", sbml_file=File(open(sbml_model_filename, "rb")))
			new_model.save()
			os.remove(sbml_model_filename)

			doc = SbmlDocument()
			doc.model.newModel("My first model")
			doc.writeSbmlToFile(os.path.join(settings.MEDIA_ROOT, str(new_model.sbml_file)))

class Project(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=255, null=True)
	folder = models.CharField(max_length=255, default=new_project_folder)
	PUBLIC = 'PU'
	PRIVATE = 'PR'

	ACCESS_CHOICES = (
		(PUBLIC, 'Public'),
		(PRIVATE, 'Private'),
	)

	access = models.CharField(max_length=2, choices=ACCESS_CHOICES, default=PRIVATE)

class SbmlModel(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	name = models.CharField(max_length=255, null=True)
	sbml_file = models.FileField(upload_to=model_filename)


class ModelsDependency(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	model = models.ForeignKey(SbmlModel, on_delete=models.CASCADE, related_name='model')
	submodel = models.ForeignKey(SbmlModel, on_delete=models.CASCADE, related_name='submodel')
	submodel_ref = models.CharField(max_length=255, null=True)

class CombineArchiveModel(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	archive_file = models.FileField(upload_to=archive_filename)

class SEDMLSimulation(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	name = models.CharField(max_length=255, null=True)
	sedml_file = models.FileField(upload_to=sedml_filename)
	sbml_file = models.FileField(upload_to=model_filename, null=True)

class Optimization(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	model = models.ForeignKey(SbmlModel, on_delete=models.CASCADE)
	optimization_id = models.CharField(max_length=255)
	cores = models.IntegerField(default=2)

	QUEUED = 'Queued'
	INTERRUPTED = 'Interrupted'
	BUSY = 'Running'
	ENDED = 'Finished'
	ERROR = 'Failed'

	STATUSES = (
		(QUEUED, 'Queued'),
		(INTERRUPTED, 'Interrupted'),
		(BUSY, 'Busy'),
		(ENDED, 'Ended'),
		(ERROR, 'Error')
	)

	status = models.CharField(max_length=15, choices=STATUSES, default=QUEUED)
	error = models.CharField(max_length=255, default="", null=True)
	result = models.CharField(max_length=102400, default="")

class Continuation(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	model = models.ForeignKey(SbmlModel, on_delete=models.CASCADE)
	parameter = models.CharField(max_length=255, default="")

	result = models.CharField(max_length=10240, default="")
	error = models.CharField(max_length=255, default="", null=True)

	QUEUED = 'Queued'
	BUSY = 'Running'
	ENDED = 'Finished'
	ERROR = 'Failed'

	STATUSES = (
		(QUEUED, 'Queued'),
		(BUSY, 'Busy'),
		(ENDED, 'Ended'),
		(ERROR, 'Error')
	)

	status = models.CharField(max_length=15, choices=STATUSES, default=QUEUED)


class ComputationQueue(models.Model):
	OPTIM = 'Optimization'
	CONT = 'Continuation'
	SIM = 'Simulation'

	TYPES = (
		(OPTIM, 'Optimization'),
		(CONT, 'Continuation'),
		(SIM, 'Simulation')
	)

	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	type = models.CharField(max_length=12, choices=TYPES, null=True)
	computation_id = models.IntegerField(default=-1)
	object = models.CharField(max_length=102400, default="")
	timeout = models.IntegerField(blank=True, null=True)

#######################################################################################
# Experimental data v2
#######################################################################################
class Experiment(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	notes = models.CharField(max_length=2048, null=True)

class Condition(models.Model):
	experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	notes = models.CharField(max_length=2048, null=True)


class Observation(models.Model):
	condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
	species = models.CharField(max_length=255)

	time = models.FloatField()
	value = models.FloatField()
	stddev = models.FloatField()
	steady_state = models.BooleanField()
	min_steady_state = models.FloatField(null=True)
	max_steady_state = models.FloatField(null=True)

	def create(cls, species, time, value, stddev, steady_state, min_steady_state, max_steady_state):
		data_point = cls(species=species, time=time, value=value, stddev=stddev,
							steady_state=steady_state,
							min_steady_state=min_steady_state,
							max_steady_state=max_steady_state)
		return data_point

class Treatment(models.Model):
	condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
	species = models.CharField(max_length=255)

	time = models.FloatField()
	value = models.FloatField()

	def create(cls, species, time, value):
		data_point = cls(species=species, time=time, value=value)
		return data_point
