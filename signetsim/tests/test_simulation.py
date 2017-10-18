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

from signetsim.models import User, Project, SbmlModel, SEDMLSimulation

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

		saved_simulation = SEDMLSimulation.objects.filter(project=project)[0]

		response_load_saved_simulation = c.get('/simulate/stored/%d/' % saved_simulation.id)
		self.assertEqual(response_load_saved_simulation.status_code, 200)
		self.assertEqual(
			response_load_saved_simulation.context['plots_2d'][0].listOfCurves[0].getXData(),
			[
				0.0, 60.0, 120.0, 180.0, 240.0, 300.0, 360.0, 420.0, 480.0, 540.0, 600.0, 660.0, 720.0, 780.0, 840.0,
				900.0, 960.0, 1020.0, 1080.0, 1140.0, 1200.0, 1260.0, 1320.0, 1380.0, 1440.0, 1500.0, 1560.0, 1620.0,
				1680.0, 1740.0, 1800.0, 1860.0, 1920.0, 1980.0, 2040.0, 2100.0, 2160.0, 2220.0, 2280.0, 2340.0, 2400.0,
				2460.0, 2520.0, 2580.0, 2640.0, 2700.0, 2760.0, 2820.0, 2880.0, 2940.0, 3000.0, 3060.0, 3120.0, 3180.0,
				3240.0, 3300.0, 3360.0, 3420.0, 3480.0, 3540.0, 3600.0
			]
		)

		expected_data = [
			64.5, 17.2464109961605, 15.5282325008815, 15.47923160635323, 15.47784648881911, 15.47780734534836,
			15.47780623916044, 15.47780620789976, 15.47780620701633, 15.47780620699137, 15.47780620699066,
			15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066,
			15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066,
			15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066,
			15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066,
			15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066,
			15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066,
			15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066,
			15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066,
			15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066,
			15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066, 15.47780620699066
		]

		for i, y in enumerate(expected_data):
			self.assertAlmostEqual(
				response_load_saved_simulation.context['plots_2d'][0].listOfCurves[0].getYData()[i],
				y, delta=y*1e-3
			)

		expected_data = [
			3.5, 1.939636741974183, 0.5366336676714942, 0.5164042464041984, 1.5465486512506, 0.7558169474328414,
			0.4472116865099089, 1.199333304520827, 0.9196352289926222, 0.4556369972007844, 0.9553572121949728,
			1.056377014749335, 0.4920733586578617, 0.7728476401956885, 1.159217035896495, 0.5507318055447671,
			0.6393142258106698, 1.210350843340104, 0.6304133290154413, 0.549270003550934, 1.19476869980983,
			0.7296867141561884, 0.497495718640003, 1.11301902257825, 0.8445952908088706, 0.4787798883212827,
			0.9849745684311543, 0.9664732938526834, 0.4888437929329168, 0.840576840466717, 1.080179499339999,
			0.5248113680450608, 0.7068131748466558, 1.164315712887362, 0.5849486959100987, 0.6004494123004745,
			1.19596775596856, 0.6677778085235032, 0.5279107848664328, 1.161125482951264, 0.770634917220128,
			0.4889310484797591, 1.064961220980647, 0.887717245633495, 0.4805239012302878, 0.9311512546914948,
			1.007929548454806, 0.4995823775262134, 0.7898393577951964, 1.113525084644389, 0.5438945813315644,
			0.6653113262614232, 1.181565863076041, 0.6119790238395305, 0.5709149521783061, 1.190732085754832,
			0.7021199429932027, 0.5105434333519248, 1.132830266493662, 0.8107729197435227, 0.4827297071421199
		]

		for i, y in enumerate(expected_data):
			self.assertAlmostEqual(
				response_load_saved_simulation.context['plots_2d'][0].listOfCurves[1].getYData()[i],
				y, delta=y*1e-3
			)

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
