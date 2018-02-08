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

""" test_optimization.py

	This file...

"""

from django.test import TestCase, Client
from django.conf import settings

from libsignetsim import SbmlDocument

from signetsim.models import User, Project, SbmlModel

from os.path import dirname, join
from shutil import rmtree
from time import sleep
from json import loads

class TestOptimization(TestCase):

	fixtures = ["user_with_project.json"]

	def testOptimization(self):

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

		response_create_experiment = c.post('/data/', {
			'action': 'save',
			'experiment_id': "",
			'experiment_name': "Enzymatic reaction",
			'experiment_notes': "Something"
		})

		self.assertEqual(response_create_experiment.status_code, 200)
		self.assertEqual(
			[experiment.name for experiment in response_create_experiment.context['experimental_data']],
			[u'Enzymatic reaction']
		)

		experiment_id = response_create_experiment.context['experimental_data'][0].id
		# Testing conditions

		response_choose_experiment = c.get('/data/%d/' % experiment_id)
		self.assertEqual(response_choose_experiment.status_code, 200)
		self.assertEqual(response_choose_experiment.context['experiment_name'], u'Enzymatic reaction')
		self.assertEqual(
			[condition.name for condition in response_choose_experiment.context['conditions']],
			[]
		)

		response_new_condition = c.post('/data/%d/' % experiment_id, {
			'action': 'save',
			'condition_id': "",
			'condition_name': "Test condition",
			'condition_notes': "Some notes"
		})

		self.assertEqual(response_new_condition.status_code, 200)
		self.assertEqual(
			[condition.name for condition in response_new_condition.context['conditions']],
			[u'Test condition']
		)

		condition_id = response_new_condition.context['conditions'][0].id

		response_choose_experiment = c.get('/data/%d/%d/' % (experiment_id, condition_id))
		self.assertEqual(response_choose_experiment.status_code, 200)
		self.assertEqual(len(response_choose_experiment.context['experiment_initial_data']), 0)

		response_add_treatment = c.post('/data/%d/%d/' % (experiment_id, condition_id), {
			'data_type': 'treatment',
			'action': 'save',
			'id': "",
			'name': 'Substrate',
			'time': 0,
			'value': 15
		})

		self.assertEqual(response_add_treatment.status_code, 200)
		self.assertEqual(len(response_add_treatment.context['experiment_initial_data']), 1)

		self.assertEqual(len(response_add_treatment.context['experiment_data']), 0)

		response_add_observation = c.post('/data/%d/%d/' % (experiment_id, condition_id), {
			'data_type': 'observation',
			'action': 'save',
			'id': "",
			'name': 'Product',
			'time': 0,
			'value': 0,
			'stddev': 0,
			'steady_state': 'off',
			'min_steady_state': "0",
			'max_steady_state': "0"
		})

		self.assertEqual(response_add_observation.status_code, 200)
		self.assertEqual(len(response_add_observation.context['experiment_data']), 1)

		response_add_observation = c.post('/data/%d/%d/' % (experiment_id, condition_id), {
			'data_type': 'observation',
			'action': 'save',
			'id': "",
			'name': 'Product',
			'time': 10,
			'value': 10,
			'stddev': 0,
			'steady_state': 'off',
			'min_steady_state': "0",
			'max_steady_state': "0"
		})

		self.assertEqual(response_add_observation.status_code, 200)
		self.assertEqual(len(response_add_observation.context['experiment_data']), 2)

		response_add_observation = c.post('/data/%d/%d/' % (experiment_id, condition_id), {
			'data_type': 'observation',
			'action': 'save',
			'id': "",
			'name': 'Product',
			'time': 20,
			'value': 15,
			'stddev': 0,
			'steady_state': 'off',
			'min_steady_state': "0",
			'max_steady_state': "0"
		})

		self.assertEqual(response_add_observation.status_code, 200)
		self.assertEqual(len(response_add_observation.context['experiment_data']), 3)

		response_add_observation = c.post('/data/%d/%d/' % (experiment_id, condition_id), {
			'data_type': 'observation',
			'action': 'save',
			'id': "",
			'name': 'Product',
			'time': 50,
			'value': 15,
			'stddev': 0,
			'steady_state': 'off',
			'min_steady_state': "0",
			'max_steady_state': "0"
		})

		self.assertEqual(response_add_observation.status_code, 200)
		self.assertEqual(len(response_add_observation.context['experiment_data']), 4)

		response_get_fit_data = c.get('/fit/data/')
		self.assertEqual(response_get_fit_data.status_code, 200)
		self.assertEqual(
			[dataset for dataset in response_get_fit_data.context['experimental_data_sets']],
			[u'Enzymatic reaction']
		)

		response_list_optimizations = c.get('/fit/list/')
		self.assertEqual(response_list_optimizations.status_code, 200)
		self.assertEqual(len(response_list_optimizations.context['optimizations']), 0)

		response_add_dataset = c.post('/json/add_dataset/', {
			'dataset_ind': 0
		})

		self.assertEqual(response_add_dataset.status_code, 200)
		mapping = loads(response_add_dataset.content)['model_xpaths']

		sbml_filename = str(SbmlModel.objects.filter(project=project)[0].sbml_file)

		doc = SbmlDocument()
		doc.readSbmlFromFile(join(settings.MEDIA_ROOT, sbml_filename))

		self.assertEqual(mapping.keys(), ['Product', 'Substrate'])

		self.assertEqual(doc.model.listOfSpecies.index(doc.getByXPath(mapping['Substrate'])), 0)
		self.assertEqual(doc.model.listOfSpecies.index(doc.getByXPath(mapping['Product'])), 3)

		response_create_optimization = c.post('/fit/data/', {
			'action': 'create',
			'dataset_0': experiment_id,
			'list_dataset_0_data_species_0_value': "Product",
			'list_dataset_0_species_0_value': 3,
			'list_dataset_0_data_species_1_value': "Substrate",
			'list_dataset_0_species_1_value': 0,
			'parameter_0_active': "on",
			'parameter_0_id': 0,
			'parameter_0_name': "Binding rate",
			'parameter_0_value': 1.0,
			'parameter_0_min': 1e-4,
			'parameter_0_max': 1e+4,
			'parameter_0_precision': 7,
			'parameter_1_active': "on",
			'parameter_1_id': 0,
			'parameter_1_name': "Unbinding rate",
			'parameter_1_value': 1.0,
			'parameter_1_min': 1e-4,
			'parameter_1_max': 1e+4,
			'parameter_1_precision': 7,
			'parameter_2_active': "on",
			'parameter_2_id': 0,
			'parameter_2_name': "Catalytic rate",
			'parameter_2_value': 1.0,
			'parameter_2_min': 1e-4,
			'parameter_2_max': 1e+4,
			'parameter_2_precision': 7,

			'nb_cores': 2,
			'lambda': 0.001,
			'score_precision': 0.001,
			'param_precision': 7,
			'initial_temperature': 1,
			'initial_moves': 2000,
			'freeze_count': 100,
			'negative_penalty': 0
		})

		self.assertEqual(response_create_optimization.status_code, 200)
		self.assertEqual(response_create_optimization.context['form'].getErrors(), [])

		sleep(5)

		response_list_optimizations = c.get('/fit/list/')
		self.assertEqual(response_list_optimizations.status_code, 200)
		self.assertEqual(len(response_list_optimizations.context['optimizations']), 1)
		self.assertEqual(response_list_optimizations.context['optimizations'][0][1], "Ongoing")

		sleep(10)

		response_get_optimization = c.get('/fit/%s/' % response_list_optimizations.context['optimizations'][0][0].optimization_id)
		self.assertEqual(response_get_optimization.status_code, 200)

		sleep(240)

		response_list_optimizations = c.get('/fit/list/')
		self.assertEqual(response_list_optimizations.status_code, 200)
		self.assertEqual(response_list_optimizations.context['optimizations'][0][1], "Finished")

		response_get_optimization = c.get(
			'/fit/%s/' % response_list_optimizations.context['optimizations'][0][0].optimization_id)
		self.assertEqual(response_get_optimization.status_code, 200)

		scores = response_get_optimization.context['score_values']
		self.assertTrue(scores[len(scores)-1] < 0.24)