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

""" test_validators.py

	This file...

"""

from django.conf import settings
from django.test import TestCase, Client

from signetsim.models import User, Project, SbmlModel

from os.path import dirname, join
from json import loads


class TestValidators(TestCase):

	fixtures = ["user_with_project.json"]

	def testValidators(self):

		user = User.objects.filter(username='test_user')[0]
		self.assertEqual(len(Project.objects.filter(user=user)), 1)
		project = Project.objects.filter(user=user)[0]
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 0)

		c = Client()
		self.assertTrue(c.login(username='test_user', password='password'))

		response_choose_project = c.get('/project/%s/' % project.folder)
		self.assertRedirects(response_choose_project, '/models/', status_code=302, target_status_code=200)

		files_folder = join(dirname(__file__), "files")
		model_filename = join(files_folder, "modelqlzB7i.xml")

		response_load_model = c.post('/models/', {
			'action': 'load_model',
			'docfile': open(model_filename, 'r')
		})

		self.assertEqual(response_load_model.status_code, 200)
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 1)

		response_validate_float = c.post('/json/float_validator/', {
			'value': '633.656',
		})

		self.assertEqual(response_validate_float.status_code, 200)
		self.assertEqual(loads(response_validate_float.content)['error'], "")

		response_validate_float = c.post('/json/float_validator/', {
			'value': 'poil',
		})

		self.assertEqual(response_validate_float.status_code, 200)
		self.assertEqual(loads(response_validate_float.content)['error'], "isn't a float !")

		response_validate_float = c.post('/json/float_validator/', {
			'value': '',
		})

		self.assertEqual(response_validate_float.status_code, 200)
		self.assertEqual(loads(response_validate_float.content)['error'], "is empty !")

		response_validate_math = c.post('/json/math_validator/', {
			'math': 'sos+ras_gtp',
		})

		self.assertEqual(response_validate_math.status_code, 200)
		self.assertEqual(loads(response_validate_math.content)['valid'], "true")

		response_validate_math = c.post('/json/math_validator/', {
			'math': 'poil*sos',
		})

		self.assertEqual(response_validate_math.status_code, 200)
		self.assertEqual(loads(response_validate_math.content)['valid'], "false")

		response_validate_math = c.post('/json/math_validator/', {
			'math': 'poil sos',
		})

		self.assertEqual(response_validate_math.status_code, 200)
		self.assertEqual(loads(response_validate_math.content)['valid'], "false")

		response_validate_sbml_id = c.post('/json/sbml_id_validator/', {
			'sbml_id': 'sos',
		})

		self.assertEqual(response_validate_sbml_id.status_code, 200)
		self.assertEqual(loads(response_validate_sbml_id.content)['error'], "sbml id already exists")

		response_validate_sbml_id = c.post('/json/sbml_id_validator/', {
			'sbml_id': '',
		})

		self.assertEqual(response_validate_sbml_id.status_code, 200)
		self.assertEqual(loads(response_validate_sbml_id.content)['error'], "sbml id is not valid")

		response_validate_sbml_id = c.post('/json/sbml_id_validator/', {
			'sbml_id': 'fw+*f',
		})

		self.assertEqual(response_validate_sbml_id.status_code, 200)
		self.assertEqual(loads(response_validate_sbml_id.content)['error'], "sbml id is not valid")

		response_validate_unit_id = c.post('/json/unit_id_validator/', {
			'unit_id': 'fw+*f',
		})

		self.assertEqual(response_validate_unit_id.status_code, 200)
		self.assertEqual(loads(response_validate_unit_id.content)['valid'], "false")

		response_validate_unit_id = c.post('/json/unit_id_validator/', {
			'unit_id': 'L',
		})

		self.assertEqual(response_validate_unit_id.status_code, 200)
		self.assertEqual(loads(response_validate_unit_id.content)['valid'], "false")

		response_validate_unit_id = c.post('/json/unit_id_validator/', {
			'unit_id': 'LL',
		})

		self.assertEqual(response_validate_unit_id.status_code, 200)
		self.assertEqual(loads(response_validate_unit_id.content)['valid'], "true")
# model = SbmlModel.objects.filter(project=project)[0]
		# sbml_doc = SbmlDocument()
		# sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		# sbml_model = sbml_doc.getModelInstance()
		#
