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

""" test_units.py

	This file...

"""

from django.conf import settings
from django.test import TestCase, Client

from signetsim.models import User, Project, SbmlModel

from libsignetsim import SbmlDocument
from libsignetsim.model.sbml.Unit import Unit

from os.path import dirname, join
from json import loads


class TestUnits(TestCase):

	fixtures = ["user_with_project.json"]

	def testUnits(self):

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
			'docfile': open(model_filename, 'rb')
		})

		self.assertEqual(response_load_model.status_code, 200)
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 1)

		model = SbmlModel.objects.filter(project=project)[0]
		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()

		response_choose_project = c.post('/models/', {
			'action': 'choose_project',
			'project_id': 0
		})
		self.assertEqual(response_choose_project.status_code, 200)
		self.assertEqual(response_choose_project.context['project_name'], "Project")

		response_choose_model = c.post('/edit/units/', {
			'action': 'choose_model',
			'model_id': 0
		})
		self.assertEqual(response_choose_model.status_code, 200)
		self.assertEqual(response_choose_model.context['model_name'], "SOS-Ras-MAPK with n17")

		self.assertEqual(
			response_choose_model.context['unit_definitions'],
			['Litre', 'Nanomoles', 'Nanomoles per litre', 'Seconds', 'per Seconds', 'per Nanomoles ', 'Dimensionless',
			 'per Nanomoles per Seconds', 'Nanomoles per seconds', 'Nanomoles per litre per seconds',
			 'per Nanomoles per liter per Seconds']
		)

		response_save_unit = c.post('/edit/units/', {
			'action': 'save',
			'unit_definition_id': '',
			'unit_definition_name': "Nanomolars",
			'unit_definition_identifier': "nanomolars",
			'subunit_id_0': list(Unit.unit_id.values()).index("mole"),
			'subunit_exponent_0': 1,
			'subunit_scale_0': -9,
			'subunit_multiplier_0': 1,
			'subunit_id_1': list(Unit.unit_id.values()).index("litre"),
			'subunit_exponent_1': -1,
			'subunit_scale_1': 1,
			'subunit_multiplier_1': 1,
		})

		self.assertEqual(response_save_unit.status_code, 200)
		self.assertEqual(response_save_unit.context['form'].getErrors(), [])
		self.assertEqual(
			response_save_unit.context['unit_definitions'],
			['Litre', 'Nanomoles', 'Nanomoles per litre', 'Seconds', 'per Seconds', 'per Nanomoles ', 'Dimensionless',
			 'per Nanomoles per Seconds', 'Nanomoles per seconds', 'Nanomoles per litre per seconds',
			 'per Nanomoles per liter per Seconds', 'Nanomolars']
		)

		response_get_unit_definition = c.post('/json/get_unit_definition/', {
			'id': response_save_unit.context['unit_definitions'].index('Nanomolars'),
		})
		self.assertEqual(response_get_unit_definition.status_code, 200)
		json_response = loads(response_get_unit_definition.content.decode('utf-8'))

		self.assertEqual(json_response[u'unit_id'], "nanomolars")
		self.assertEqual(json_response[u'name'], "Nanomolars")
		self.assertEqual(json_response[u'desc'], "nmole.litre^-1")
		self.assertEqual(json_response[u'list_of_units'][0], [u'nmole', 20, u'mole', 1, -9, 1.0])
		self.assertEqual(json_response[u'list_of_units'][1], [u'litre^-1', 16, u'litre', -1, 1, 1.0])

		response_delete_unit_definition = c.post('/edit/units/', {
			'action': 'delete',
			'id': response_save_unit.context['unit_definitions'].index('Nanomolars')
		})

		self.assertEqual(response_delete_unit_definition.status_code, 200)
		self.assertEqual(
			response_delete_unit_definition.context['unit_definitions'],
			['Litre', 'Nanomoles', 'Nanomoles per litre', 'Seconds', 'per Seconds', 'per Nanomoles ', 'Dimensionless',
			 'per Nanomoles per Seconds', 'Nanomoles per seconds', 'Nanomoles per litre per seconds',
			 'per Nanomoles per liter per Seconds']
		)
