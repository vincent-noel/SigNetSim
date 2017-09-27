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
from django.conf import settings

from signetsim.models import User, Project, SbmlModel, Experiment, SEDMLSimulation
from libsignetsim.combine.CombineArchive import CombineArchive

from os.path import dirname, join
from shutil import rmtree


class TestSimulation(TestCase):

	fixtures = ["user_with_project.json"]

	def testTimeseries(self):

		settings.MEDIA_ROOT = "/tmp/"

		user = User.objects.filter(username='test_user')[0]
		self.assertEqual(len(Project.objects.filter(user=user)), 1)
		project = Project.objects.filter(user=user)[0]

		# This test can only run once with success, because the second time the comp model dependencies will
		# actually be in the folder. So cleaning the project folder now
		rmtree(join(join(settings.MEDIA_ROOT, str(project.folder))), "models")

		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 0)

		c = Client()
		self.assertTrue(c.login(username='test_user', password='password'))

		response_choose_project = c.get('/project/%s/' % project.folder)
		self.assertRedirects(response_choose_project, '/models/', status_code=302, target_status_code=200)

		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 0)

		files_folder = join(dirname(__file__), "files")
		model_filename = join(files_folder, "modelqlzB7i.xml")

		response_load_model = c.post('/models/', {
			'action': 'load_model',
			'docfile': open(model_filename, 'r')
		})

		self.assertEqual(response_load_model.status_code, 200)
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 1)

		response_simulate_model = c.post('/simulate/timeseries/', {
			'action': 'simulate_model',
			'species_selected': [2, 21],
			'experiment_id': "",
			'time_min': 0,
			'time_ech': 60,
			'time_max': 3600
		})

		self.assertEqual(response_simulate_model.status_code, 200)
		self.assertEqual(response_simulate_model.context['form'].getErrors(), [])

		self.assertEqual(len(SEDMLSimulation.objects.filter(project=project)), 0)
		response_save_simulation = c.post('/simulate/timeseries/', {
			'action': 'save_simulation',
			'species_selected': [2, 21],
			'experiment_id': "",
			'time_min': 0,
			'time_ech': 60,
			'time_max': 3600
		})

		self.assertEqual(response_save_simulation.status_code, 200)
		self.assertEqual(response_save_simulation.context['form'].getErrors(), [])
		self.assertEqual(len(SEDMLSimulation.objects.filter(project=project)), 1)

	def testSteadyStates(self):

		settings.MEDIA_ROOT = "/tmp/"

		user = User.objects.filter(username='test_user')[0]
		self.assertEqual(len(Project.objects.filter(user=user)), 1)
		project = Project.objects.filter(user=user)[0]

		# This test can only run once with success, because the second time the comp model dependencies will
		# actually be in the folder. So cleaning the project folder now
		rmtree(join(join(settings.MEDIA_ROOT, str(project.folder))), "models")

		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 0)

		c = Client()
		self.assertTrue(c.login(username='test_user', password='password'))

		response_choose_project = c.get('/project/%s/' % project.folder)
		self.assertRedirects(response_choose_project, '/models/', status_code=302, target_status_code=200)

		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 0)

		files_folder = join(dirname(__file__), "files")
		model_filename = join(files_folder, "modelx8Ow70.xml")

		response_load_model = c.post('/models/', {
			'action': 'load_model',
			'docfile': open(model_filename, 'r')
		})

		self.assertEqual(response_load_model.status_code, 200)
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 1)

		response_get_steady_states = c.get('/simulate/steady_states/')
		self.assertEqual(response_get_steady_states.status_code, 200)

		response_simulate_model = c.post('/simulate/steady_states/', {
			'action': 'simulate_steady_states',
			'species_selected': [0, 1, 2, 3],
			'species_id': [species.getSbmlId() for species in response_get_steady_states.context['species']].index('substrate'),
			'ss_to_plot': "0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
			'time_max': 1000
		})

		self.assertEqual(response_simulate_model.status_code, 200)
		self.assertEqual(response_simulate_model.context['form'].getErrors(), [])

		for i in range(11):
			self.assertAlmostEqual(response_simulate_model.context['sim_results']['ES-complex'][i], 0)
			self.assertAlmostEqual(response_simulate_model.context['sim_results']['Enzyme'][i], 10)
			self.assertAlmostEqual(response_simulate_model.context['sim_results']['Substrate'][i], 0)

		self.assertAlmostEqual(response_simulate_model.context['sim_results']['Product'][0], 0)
		self.assertAlmostEqual(response_simulate_model.context['sim_results']['Product'][1], 1)
		self.assertAlmostEqual(response_simulate_model.context['sim_results']['Product'][2], 2)
		self.assertAlmostEqual(response_simulate_model.context['sim_results']['Product'][3], 3)
		self.assertAlmostEqual(response_simulate_model.context['sim_results']['Product'][4], 4)
		self.assertAlmostEqual(response_simulate_model.context['sim_results']['Product'][5], 5)
		self.assertAlmostEqual(response_simulate_model.context['sim_results']['Product'][6], 6)
		self.assertAlmostEqual(response_simulate_model.context['sim_results']['Product'][7], 7)
		self.assertAlmostEqual(response_simulate_model.context['sim_results']['Product'][8], 8)
		self.assertAlmostEqual(response_simulate_model.context['sim_results']['Product'][9], 9)
		self.assertAlmostEqual(response_simulate_model.context['sim_results']['Product'][10], 10)
