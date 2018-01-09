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

from os.path import isdir, join, exists, getsize, isfile
from os import kill, getcwd, setpgrp
from shutil import rmtree
from django.conf import settings
from subprocess import check_call, check_output
from glob import glob


def deleteOptimization(optimization):

	subdirectory = "optimization_%s" % optimization.optimization_id
	directory = join(settings.MEDIA_ROOT, optimization.project.folder, "optimizations", subdirectory)
	if isdir(directory):
		rmtree(directory)
	optimization.delete()


def getOptimizationStatus(optim_path):

	optimization_status = None

	if not exists(optim_path):
		optimization_status = "Not found"

	elif isfile(optim_path + "/logs/score/score"):
		optimization_status = "Finished"

	elif isfile(optim_path + "/err_optim") and getsize(optim_path + "/err_optim") > 0:
		optimization_status = "Failed"

	else:
		try:
			with open(join(optim_path, "pid")) as f:
				pid = f.read()
				check_output(['pwdx', pid])#, stdout=None, stderr=None)
				optimization_status = "Ongoing"

		except:
			optimization_status = "Interrupted"

	return optimization_status


def stopOptimization(optim_path):

	if isfile(join(optim_path, "pid")):
		t_pidfile = open(join(optim_path, "pid"), "r")
		t_pid = int(t_pidfile.readline().strip())
		kill(t_pid, 9)

def restartOptimization(optim_path):

	nb_procs = len(glob(join(optim_path, 'plsa_*.state')))
	present_dir = getcwd()

	if nb_procs > 1 and isfile(join(optim_path, "lsa.mpi")):
		target = "cd %s; mpirun -np %d ./lsa.mpi; cd %s" % (optim_path, nb_procs, present_dir)

	else:
		target = "cd %s; ./lsa; cd %s" % (optim_path, present_dir)

	check_call(target,
		stdout=open(join(optim_path, "out_optim"), "w"),
		stderr=open(join(optim_path, "err_optim"), "w"),
		shell=True, preexec_fn=setpgrp, close_fds=True
	)
