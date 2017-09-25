#!/usr/bin/env python
""" test_simulation.py


	This file...



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
		model_filename = join(files_folder, "modelqlzB7i.xml")

		response_load_model = c.post('/models/', {
			'action': 'load_model',
			'docfile': open(model_filename, 'r')
		})

		self.assertEqual(response_load_model.status_code, 200)
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 1)

