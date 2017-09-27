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

""" test_biomodels.py

	This file...

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

		self.assertTrue('results' in json_response.keys() or 'error' in json_response.keys())

		if not 'error' in json_response.keys():
			self.assertTrue(len(json_response['results']) >= 11)

			self.assertEqual(json_response['results'][0], u"BIOMD0000000005")
			self.assertEqual(json_response['results'][1], u"BIOMD0000000006")
			self.assertEqual(json_response['results'][2], u"BIOMD0000000036")
			self.assertEqual(json_response['results'][3], u"BIOMD0000000195")
			self.assertEqual(json_response['results'][4], u"BIOMD0000000306")
			self.assertEqual(json_response['results'][5], u"BIOMD0000000307")
			self.assertEqual(json_response['results'][6], u"BIOMD0000000308")
			self.assertEqual(json_response['results'][7], u"BIOMD0000000309")
			self.assertEqual(json_response['results'][8], u"BIOMD0000000310")
			self.assertEqual(json_response['results'][9], u"BIOMD0000000311")
			self.assertEqual(json_response['results'][10], u"BIOMD0000000312")

		response_load_tyson = c.post('/models/', {
			'action': 'load_biomodels',
			'model_id': 'BIOMD0000000005'
		})

		self.assertEqual(response_load_tyson.status_code, 200)
		self.assertTrue(
			len(SbmlModel.objects.filter(project=project)) == 1
			or response_load_tyson.context['getErrors'] == ["Unable to load model from biomodels"]
		)

		if not response_load_tyson.context['getErrors'] == ["Unable to load model from biomodels"]:
			self.assertEqual(
				response_load_tyson.context['sbml_models'][0][1],
				u'Tyson1991 - Cell Cycle 6 var'
			)

		#Should not work because of the non-ascii character for TGF-beta
		response_import_unicode = c.post('/models/', {
			'action': 'load_biomodels',
			'model_id': 'BIOMD0000000342'
		})
		self.assertEqual(response_import_unicode.status_code, 200)

