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

	def testTimeseriesCompModel(self):

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
		comp_files_folder = join(files_folder, "comp_model")

		model_filename = join(comp_files_folder, "modelcEvRcX.xml")
		response_load_submodel_1 = c.post('/models/', {
			'action': 'load_model',
			'docfile': open(model_filename, 'r')
		})

		self.assertEqual(response_load_submodel_1.status_code, 200)
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 1)

		model_filename = join(comp_files_folder, "modelEHfev9.xml")
		response_load_submodel_2 = c.post('/models/', {
			'action': 'load_model',
			'docfile': open(model_filename, 'r')
		})

		self.assertEqual(response_load_submodel_2.status_code, 200)
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 2)

		model_filename = join(comp_files_folder, "modelI1vrys.xml")
		response_load_submodel_3 = c.post('/models/', {
			'action': 'load_model',
			'docfile': open(model_filename, 'r')
		})

		self.assertEqual(response_load_submodel_3.status_code, 200)
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 3)

		model_filename = join(comp_files_folder, "modelz9xdww.xml")

		response_load_model = c.post('/models/', {
			'action': 'load_model',
			'docfile': open(model_filename, 'r')
		})

		self.assertEqual(response_load_model.status_code, 200)
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 4)

		experiment_filename = join(files_folder, "ras_data.xml")

		response_import_data = c.post('/data/', {
			'action': 'import',
			'docfile': open(experiment_filename, 'r')
		})

		self.assertEqual(response_import_data.status_code, 200)
		self.assertEqual(
			[experiment.name for experiment in response_import_data.context['experimental_data']],
			[u'Ras-GTP quantifications']
		)

		response_choose_model = c.post('/simulate/timeseries/', {
			'action': 'choose_model',
			'model_id': 3
		})

		self.assertEqual(response_choose_model.status_code, 200)

		self.assertEqual(
			[species.getName() for species in response_choose_model.context['species']],
			['SOS', 'Ras-GTP', 'ERK-PP', 'SOS_inactive', 'FGF2', 'Ras-GDP', 'SOS-Ras-GDP', 'SOS-Ras-GTP', 'GAP', 'GEF',
			 'Ras-N17', 'SOS-Ras-N17', 'GEF-RasN17', 'Total Ras-GTP', 'Raf', 'Raf-P', 'Mek', 'Mek-P', 'Mek-PP', 'Mapk',
			 'Mapk-P', 'Total MEK activated', 'Total MAPK activated']
		)

		self.assertEqual(
			[experiment.name for experiment in response_choose_model.context['experiments']],
			[u'Ras-GTP quantifications']
		)

		response_simulate_model = c.post('/simulate/timeseries/', {
			'action': 'simulate_model',
			'species_selected': [2, 21],
			'experiment_id': 0,
			'time_min': 0,
			'time_ech': 60,
			'time_max': 360
		})

		self.assertEqual(response_simulate_model.status_code, 200)
		self.assertEqual(response_simulate_model.context['form'].getErrors(), [])

		self.assertEqual(len(response_simulate_model.context['sim_results']), 2)

		self.assertEqual(
			response_simulate_model.context['sim_results'][0][0],
			[0.0, 60.0, 120.0, 180.0, 240.0, 300.0, 360.0]
		)

		self.assertEqual(
			response_simulate_model.context['sim_results'][1][0],
			[0.0, 60.0, 120.0, 180.0, 240.0, 300.0, 360.0]
		)

		self.assertEqual(
			response_simulate_model.context['sim_results'][0][1].keys(),
			[u'Total MEK activated', u'ERK-PP']
		)
		self.assertEqual(
			response_simulate_model.context['sim_results'][1][1].keys(),
			[u'Total MEK activated', u'ERK-PP']
		)

		self.assertEqual(
			[name for _, _, name in response_simulate_model.context['sim_results']],
			[u'Starved', u'FGF2']
		)


		self.assertEqual(len(SEDMLSimulation.objects.filter(project=project)), 0)
		response_save_simulation = c.post('/simulate/timeseries/', {
			'action': 'save_simulation',
			'species_selected': [2, 21],
			'experiment_id': 0,
			'time_min': 0,
			'time_ech': 60,
			'time_max': 360
		})

		self.assertEqual(response_save_simulation.status_code, 200)
		self.assertEqual(response_save_simulation.context['form'].getErrors(), [])
		self.assertEqual(len(SEDMLSimulation.objects.filter(project=project)), 1)

		saved_simulation = SEDMLSimulation.objects.filter(project=project)[0]

		response_load_saved_simulation = c.get('/simulate/stored/%d/' % saved_simulation.id)
		self.assertEqual(response_load_saved_simulation.status_code, 200)
		self.assertEqual(
			response_load_saved_simulation.context['plots_2d'][0].listOfCurves[0].getXData(),
			[0.0, 60.0, 120.0, 180.0, 240.0, 300.0, 360.0]
		)
		expected_results = [
			3.5, 1.939636741974182, 0.5366336676714862, 0.5164042464042035, 1.546548651250602, 0.7558169474328419,
			0.4472116865099191
		]
		for i, y in enumerate(expected_results):
			self.assertAlmostEqual(
				response_load_saved_simulation.context['plots_2d'][0].listOfCurves[0].getYData()[i],
				y, delta=y*1e-3
			)

		expected_results = [
			30.0, 14.81260866089722, 8.165121865009306, 20.47692478996913, 24.42348326555909, 11.41597504856704,
			15.96502932122009
		]
		for i, y in enumerate(expected_results):
			self.assertAlmostEqual(
				response_load_saved_simulation.context['plots_2d'][0].listOfCurves[1].getYData()[i],
				y, delta=y*1e-3
			)
