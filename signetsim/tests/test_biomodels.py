#!/usr/bin/env python
""" test_biomodels.py


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
from json import loads


class TestBiomodels(TestCase):

	fixtures = ["user_with_project.json"]

	def testImportModel(self):

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

		response_search_tyson = c.post('/json/search_biomodels/', {
			'search_type': 0,
			'search_string': "tyson"
		})

		self.assertEqual(response_search_tyson.status_code, 200)
		json_response = loads(response_search_tyson.content)

		self.assertTrue('results' in json_response.keys())
		self.assertTrue(len(json_response['results']) >= 11)
		self.assertEqual(json_response['results'][0], ["BIOMD0000000005", "Tyson1991 - Cell Cycle 6 var"])
		self.assertEqual(json_response['results'][1], ["BIOMD0000000006", "Tyson1991 - Cell Cycle 2 var"])
		self.assertEqual(json_response['results'][2], ["BIOMD0000000036", "Tyson1999_CircClock"])
		self.assertEqual(json_response['results'][3], ["BIOMD0000000195", "Tyson2001_Cell_Cycle_Regulation"])
		self.assertEqual(json_response['results'][4], ["BIOMD0000000306", "Tyson2003_Activator_Inhibitor"])
		self.assertEqual(json_response['results'][5], ["BIOMD0000000307", "Tyson2003_Substrate_Depletion_Osc"])
		self.assertEqual(json_response['results'][6], ["BIOMD0000000308", "Tyson2003_NegFB_Oscillator"])
		self.assertEqual(json_response['results'][7], ["BIOMD0000000309", "Tyson2003_NegFB_Homeostasis"])
		self.assertEqual(json_response['results'][8], ["BIOMD0000000310", "Tyson2003_Mutual_Inhibition"])
		self.assertEqual(json_response['results'][9], ["BIOMD0000000311", "Tyson2003_Mutual_Activation"])
		self.assertEqual(json_response['results'][10], ["BIOMD0000000312", "Tyson2003_Perfect_Adaption"])

		response_load_tyson = c.post('/models/', {
			'action': 'load_biomodels',
			'model_id': 'BIOMD0000000005'
		})

		self.assertEqual(response_load_tyson.status_code, 200)
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 1)
		self.assertEqual(
			response_load_tyson.context['sbml_models'][0][1],
			u'Tyson1991 - Cell Cycle 6 var'
		)

		# Should not work because of the non-ascii character for TGF-beta
		# response_import_unicode = c.post('/models/', {
		# 	'action': 'load_biomodels',
		# 	'model_id': 'BIOMD0000000342'
		# })
		# self.assertEqual(response_import_unicode.status_code, 200)

