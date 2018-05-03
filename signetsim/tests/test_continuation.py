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

""" test_simulation.py

	This file...

"""

from django.test import TestCase, Client

from signetsim.models import User, Project, SbmlModel, ContinuationComputation

from os.path import dirname, join
from json import loads
from time import sleep


class TestContinuation(TestCase):

	fixtures = ["user_with_project.json"]

	def testBistable(self):

		user = User.objects.filter(username='test_user')[0]
		self.assertEqual(len(Project.objects.filter(user=user)), 1)
		project = Project.objects.filter(user=user)[0]

		c = Client()
		self.assertTrue(c.login(username='test_user', password='password'))

		response_choose_project = c.get('/project/%s/' % project.folder)
		self.assertRedirects(response_choose_project, '/models/', status_code=302, target_status_code=200)

		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 0)

		files_folder = join(dirname(__file__), "files")
		model_filename = join(files_folder, "tyson2.xml")

		response_load_model = c.post('/models/', {
			'action': 'load_model',
			'docfile': open(model_filename, 'rb')
		})

		self.assertEqual(response_load_model.status_code, 200)
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 1)
		self.assertEqual(len(ContinuationComputation.objects.filter(project=project)), 0)

		response_compute_curve = c.post('/analyse/bifurcations/', {
			'action': 'compute_curve',
			'parameter': 3,
			'variable': 1,
			'from_value': 0,
			'to_value': 5000,
			'max_steps': 1000,
			'ds': 0.1
		})

		self.assertEqual(response_compute_curve.status_code, 200)
		self.assertEqual(len(response_compute_curve.context['list_of_computations']), 1)
		self.assertEqual(len(ContinuationComputation.objects.filter(project=project)), 1)

		response_get_status = c.post('/json/get_continuation_status/', {'continuation_id': 0})

		self.assertEqual(response_get_status.status_code, 200)
		json_response = loads(response_get_status.content.decode('utf-8'))

		self.assertEqual(json_response['status'], 'BU')

		sleep(30)

		response_get_status = c.post('/json/get_continuation_status/', {'continuation_id': 0})

		self.assertEqual(response_get_status.status_code, 200)
		json_response = loads(response_get_status.content.decode('utf-8'))

		# we cannot really test, because the test database doesn't like threads.
		# Maybe we could find a trick for that, but for now i will give up
	
		# print(json_response)
		# response_get_curve = c.post('/json/get_equilibrium_curve/', {'id': 0})
		#
		# self.assertEqual(response_get_curve.status_code, 200)
		# json_response = loads(response_get_curve.content.decode('utf-8'))
		#
		# print(json_response)