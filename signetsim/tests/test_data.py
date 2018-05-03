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

""" test_data.py

	This file...

"""

from django.test import TestCase, Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings

from signetsim.models import User, Project, SbmlModel
from signetsim.views.ListOfModelsView import ListOfModelsView

from os.path import dirname, join
from shutil import rmtree
from json import loads


class TestData(TestCase):

	fixtures = ["user_with_project.json"]

	def testImportData(self):

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

		files_folder = join(dirname(__file__), "files")
		experiment_filename = join(files_folder, "experiment.xml")

		response_import_data = c.post('/data/', {
			'action': 'import',
			'docfile': open(experiment_filename, 'r')
		})

		self.assertEqual(response_import_data.status_code, 200)
		self.assertEqual(
			[experiment.name for experiment in response_import_data.context['experimental_data']],
			[u'Ras, Mapk quantifications']
		)


		response_create_experiment = c.post('/data/', {
			'action': 'save',
			'experiment_id': "",
			'experiment_name': "Test experiment",
			'experiment_notes': "Something"
		})

		self.assertEqual(response_create_experiment.status_code, 200)
		self.assertEqual(
			[experiment.name for experiment in response_create_experiment.context['experimental_data']],
			[u'Ras, Mapk quantifications', u'Test experiment']
		)

		response_modify_experiment = c.post('/data/', {
			'action': 'save',
			'experiment_id': response_create_experiment.context['experimental_data'][1].id,
			'experiment_name': "Test experiment different",
			'experiment_notes': "Something"
		})

		self.assertEqual(response_modify_experiment.status_code, 200)
		self.assertEqual(
			[experiment.name for experiment in response_modify_experiment.context['experimental_data']],
			[u'Ras, Mapk quantifications', u'Test experiment different']
		)

		response_delete_experiment = c.post('/data/', {
			'action': 'delete',
			'id': response_create_experiment.context['experimental_data'][1].id
		})

		self.assertEqual(response_delete_experiment.status_code, 200)
		self.assertEqual(
			[experiment.name for experiment in response_delete_experiment.context['experimental_data']],
			[u'Ras, Mapk quantifications']
		)

		experiment_id = response_delete_experiment.context['experimental_data'][0].id

		response_json_get_experiment = c.post('/json/get_experiment/', {
			'id': experiment_id
		})

		self.assertEqual(response_json_get_experiment.status_code, 200)
		json_response = loads(response_json_get_experiment.content.decode('utf-8'))

		self.assertEqual(json_response[u'name'], u'Ras, Mapk quantifications')
		self.assertEqual(json_response[u'notes'], u'')

		response_download_experiment = c.get(
			'/data_archive/%d/' % experiment_id
		)

		self.assertEqual(response_download_experiment.status_code, 200)
		lines = response_download_experiment.content.decode('utf-8').split("\n")
		self.assertEqual(lines[0], "<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
		self.assertEqual(lines[1], "<numl xmlns=\"http://www.numl.org/numl/level1/version1\" level=\"1\" version=\"1\">")

		response_duplicate_experiment = c.post('/data/', {
			'action': 'duplicate',
			'id': experiment_id
		})

		self.assertEqual(response_duplicate_experiment.status_code, 200)
		self.assertEqual(
			[experiment.name for experiment in response_duplicate_experiment.context['experimental_data']],
			[u'Ras, Mapk quantifications', u'Ras, Mapk quantifications']
		)

		response_get_experiments_page = c.get('/data/')

		self.assertEqual(response_get_experiments_page.status_code, 200)
		self.assertEqual(
			[experiment.name for experiment in response_get_experiments_page.context['experimental_data']],
			[u'Ras, Mapk quantifications', u'Ras, Mapk quantifications']
		)



		# Testing conditions
		response_choose_experiment = c.get('/data/%d/' % experiment_id)
		self.assertEqual(response_choose_experiment.status_code, 200)
		self.assertEqual(response_choose_experiment.context['experiment_name'], u'Ras, Mapk quantifications')
		self.assertEqual(
			[condition.name for condition in response_choose_experiment.context['conditions']],
			[u'Starved', u'+Ras-N17', u'+FGF2', u'+FGF2 +Ras-N17']
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
			[u'Starved', u'+Ras-N17', u'+FGF2', u'+FGF2 +Ras-N17', u'Test condition']
		)

		condition_id = [
			condition.id
			for condition in response_new_condition.context['conditions']
			if condition.name == "Test condition"
		]

		response_modify_condition = c.post('/data/%d/' % experiment_id, {
			'action': 'save',
			'condition_id': condition_id,
			'condition_name': "Test condition, but different",
			'condition_notes': "Some modified notes"
		})

		self.assertEqual(response_modify_condition.status_code, 200)
		self.assertEqual(
			[condition.name for condition in response_modify_condition.context['conditions']],
			[u'Starved', u'+Ras-N17', u'+FGF2', u'+FGF2 +Ras-N17', u'Test condition, but different']
		)

		response_json_get_condition = c.post('/json/get_condition/', {
			'id': condition_id
		})

		self.assertEqual(response_json_get_condition.status_code, 200)
		json_response = loads(response_json_get_condition.content.decode('utf-8'))

		self.assertEqual(json_response[u'name'], u'Test condition, but different')
		self.assertEqual(json_response[u'notes'], u'Some modified notes')

		response_delete_condition = c.post('/data/%d/' % experiment_id, {
			'action': 'delete',
			'id': condition_id
		})

		self.assertEqual(response_delete_condition.status_code, 200)
		self.assertEqual(
			[condition.name for condition in response_delete_condition.context['conditions']],
			[u'Starved', u'+Ras-N17', u'+FGF2', u'+FGF2 +Ras-N17']
		)

		condition_id = response_delete_condition.context['conditions'][3].id
		response_duplicate_condition = c.post('/data/%d/' % experiment_id, {
			'action': 'duplicate',
			'id': condition_id
		})

		self.assertEqual(response_duplicate_condition.status_code, 200)
		self.assertEqual(
			[condition.name for condition in response_duplicate_condition.context['conditions']],
			[u'Starved', u'+Ras-N17', u'+FGF2', u'+FGF2 +Ras-N17', u'+FGF2 +Ras-N17']
		)

		# Testing data
		response_choose_experiment = c.get('/data/%d/%d/' % (experiment_id, condition_id))
		self.assertEqual(response_choose_experiment.status_code, 200)
		self.assertEqual(response_choose_experiment.context['experiment_name'], u'Ras, Mapk quantifications')
		self.assertEqual(response_choose_experiment.context['condition_name'], u'+FGF2 +Ras-N17')

		for treatment in response_choose_experiment.context['experiment_initial_data']:

			response_delete_treatment = c.post('/data/%d/%d/' % (experiment_id, condition_id), {
				'data_type': 'treatment',
				'action': 'delete',
				'id': treatment.id
			})

			self.assertEqual(response_delete_treatment.status_code, 200)

		response_choose_experiment = c.get('/data/%d/%d/' % (experiment_id, condition_id))
		self.assertEqual(response_choose_experiment.status_code, 200)
		self.assertEqual(len(response_choose_experiment.context['experiment_initial_data']), 0)

		response_add_treatment = c.post('/data/%d/%d/' % (experiment_id, condition_id), {
			'data_type': 'treatment',
			'action': 'save',
			'id': "",
			'name': 'FGF2',
			'time': 0,
			'value': 333.0
		})

		self.assertEqual(response_add_treatment.status_code, 200)
		self.assertEqual(len(response_add_treatment.context['experiment_initial_data']), 1)

		treatment_id = response_add_treatment.context['experiment_initial_data'][0].id
		response_get_treatment = c.post('/json/get_treatment/', {
			'id': treatment_id
		})

		self.assertEqual(response_get_treatment.status_code, 200)
		json_response = loads(response_get_treatment.content.decode('utf-8'))

		self.assertEqual(json_response[u'species'], u'FGF2')
		self.assertEqual(json_response[u'time'], 0)
		self.assertEqual(json_response[u'value'], 333.0)

		response_modify_treatment = c.post('/data/%d/%d/' % (experiment_id, condition_id), {
			'data_type': 'treatment',
			'action': 'save',
			'id': treatment_id,
			'name': 'Ras-GTP',
			'time': 20,
			'value': 300
		})

		self.assertEqual(response_modify_treatment.status_code, 200)
		self.assertEqual(len(response_modify_treatment.context['experiment_initial_data']), 1)

		response_get_treatment = c.post('/json/get_treatment/', {
			'id': treatment_id
		})

		self.assertEqual(response_get_treatment.status_code, 200)
		json_response = loads(response_get_treatment.content.decode('utf-8'))

		self.assertEqual(json_response[u'species'], u'Ras-GTP')
		self.assertEqual(json_response[u'time'], 20)
		self.assertEqual(json_response[u'value'], 300.0)

		self.assertEqual(len(response_modify_treatment.context['experiment_data']), 0)

		response_add_observation = c.post('/data/%d/%d/' % (experiment_id, condition_id), {
			'data_type': 'observation',
			'action': 'save',
			'id': "",
			'name': 'Ras-GTP',
			'time': 300,
			'value': 333.0,
			'stddev': 30,
			'observation_steady_state': 'off',
			'min_steady_state': "0",
			'max_steady_state': "0"
		})

		self.assertEqual(response_add_observation.status_code, 200)
		self.assertEqual(len(response_add_observation.context['experiment_data']), 1)
		observation_id = response_add_observation.context['experiment_data'][0].id

		response_get_observation = c.post('/json/get_observation/', {
			'id': observation_id
		})

		self.assertEqual(response_get_observation.status_code, 200)
		json_response = loads(response_get_observation.content.decode('utf-8'))

		self.assertEqual(json_response[u'species'], u'Ras-GTP')
		self.assertEqual(json_response[u'time'], 300)
		self.assertEqual(json_response[u'value'], 333.0)
		self.assertEqual(json_response[u'stddev'], 30.0)
		self.assertEqual(json_response[u'steady_state'], 0)
		self.assertEqual(json_response[u'min_steady_state'], 0)
		self.assertEqual(json_response[u'max_steady_state'], 0)

		response_modify_observation = c.post('/data/%d/%d/' % (experiment_id, condition_id), {
			'data_type': 'observation',
			'action': 'save',
			'id': observation_id,
			'name': 'Ras-GDP',
			'time': 3600,
			'value': 60.0,
			'stddev': 10,
			'observation_steady_state': 'on',
			'min_steady_state': "2400",
			'max_steady_state': "4800"
		})

		self.assertEqual(response_modify_observation.status_code, 200)
		self.assertEqual(len(response_modify_observation.context['experiment_data']), 1)

		response_get_observation = c.post('/json/get_observation/', {
			'id': observation_id
		})

		self.assertEqual(response_get_observation.status_code, 200)
		json_response = loads(response_get_observation.content.decode('utf-8'))

		self.assertEqual(json_response[u'species'], u'Ras-GDP')
		self.assertEqual(json_response[u'time'], 3600)
		self.assertEqual(json_response[u'value'], 60.0)
		self.assertEqual(json_response[u'stddev'], 10.0)
		self.assertEqual(json_response[u'steady_state'], 1)
		self.assertEqual(json_response[u'min_steady_state'], 2400)
		self.assertEqual(json_response[u'max_steady_state'], 4800)

		response_delete_observation = c.post('/data/%d/%d/' % (experiment_id, condition_id), {
			'data_type': 'observation',
			'action': 'delete',
			'id': observation_id
		})

		self.assertEqual(response_delete_observation.status_code, 200)
		self.assertEqual(len(response_delete_observation.context['experiment_data']), 0)
