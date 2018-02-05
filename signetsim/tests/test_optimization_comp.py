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

""" test_optimization_comp.py

	This file tests the optimization for hierarchical models

"""

from django.test import TestCase, Client
from django.conf import settings

from signetsim.models import User, Project, SbmlModel

from os.path import dirname, join
from shutil import rmtree
from time import sleep

class TestOptimization(TestCase):

	fixtures = ["user_with_project.json"]

	def testOptimization(self):

		user = User.objects.filter(username='test_user')[0]
		self.assertEqual(len(Project.objects.filter(user=user)), 1)
		project = Project.objects.filter(user=user)[0]

		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 0)

		c = Client()
		self.assertTrue(c.login(username='test_user', password='password'))

		response_choose_project = c.get('/project/%s/' % project.folder)
		self.assertRedirects(response_choose_project, '/models/', status_code=302, target_status_code=200)

		response_choose_project = c.post('/models/', {
			'action': 'choose_project',
			'project_id': 0
		})
		self.assertEqual(response_choose_project.status_code, 200)

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

		response_choose_model = c.post('/fit/data/', {
			'action': 'choose_model',
			'model_id': 3
		})
		self.assertEqual(response_choose_model.status_code, 200)
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
		experiment_id = response_import_data.context['experimental_data'][0].id

		response_get_fit_data = c.get('/fit/data/')
		self.assertEqual(response_get_fit_data.status_code, 200)
		self.assertEqual(
			[dataset for dataset in response_get_fit_data.context['experimental_data_sets']],
			[u'Ras-GTP quantifications']
		)

		response_list_optimizations = c.get('/fit/list/')
		self.assertEqual(response_list_optimizations.status_code, 200)
		self.assertEqual(len(response_list_optimizations.context['optimizations']), 0)

		# response_add_dataset = c.post('/fit/data/', {
		# 	'action': 'add_dataset',
		# 	'dataset_id': 0
		# })
		#
		# self.assertEqual(response_add_dataset.status_code, 200)
		# self.assertEqual(
		# 	response_add_dataset.context['selected_datasets_ids'],
		# 	[response_get_fit_data.context['experimental_data_sets'][0].id]
		# )

		response_create_optimization = c.post('/fit/data/', {
			'action': 'create',
			'dataset_0': experiment_id, #response_get_fit_data.context['experimental_data_sets'][0].id,

			'parameter_0_id': 1,
			'parameter_0_name': "SOS activation by FGF2",
			'parameter_0_value': 1.0,
			'parameter_0_min': 1e-4,
			'parameter_0_max': 1e+4,
			'parameter_1_active': "on",
			'parameter_1_id': 1,
			'parameter_1_name': "SOS inactivation by Mapk catalytic constant",
			'parameter_1_value': 1.0,
			'parameter_1_min': 1e-6,
			'parameter_1_max': 1e+6,

			'nb_cores': 2,
			'lambda': 1,
			'score_precision': 0.001,
			'initial_temperature': 1,
			'initial_moves': 2000,
			'freeze_count': 1,
			'negative_penalty': 0
		})

		self.assertEqual(response_create_optimization.status_code, 200)
		self.assertEqual(response_create_optimization.context['form'].getErrors(), [])
		sleep(10)

		response_list_optimizations = c.get('/fit/list/')
		self.assertEqual(response_list_optimizations.status_code, 200)
		self.assertEqual(len(response_list_optimizations.context['optimizations']), 1)
		self.assertEqual(response_list_optimizations.context['optimizations'][0][1], "Ongoing")

		sleep(10)

		optimization_id = response_list_optimizations.context['optimizations'][0][0].optimization_id
		response_get_optimization = c.get('/fit/%s/' % optimization_id)
		self.assertEqual(response_get_optimization.status_code, 200)

		sleep(180)
		response_list_optimizations = c.get('/fit/list/')
		self.assertEqual(response_list_optimizations.status_code, 200)
		self.assertEqual(response_list_optimizations.context['optimizations'][0][1], "Finished")
