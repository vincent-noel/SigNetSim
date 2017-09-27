#!/usr/bin/env python
""" test_units.py


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

from django.conf import settings
from django.test import TestCase, Client

from signetsim.models import User, Project, SbmlModel

from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.model.sbml.Unit import Unit

from os.path import dirname, join
from json import loads


class TestUnits(TestCase):

	fixtures = ["user_with_project.json"]

	def testEvents(self):

		settings.MEDIA_ROOT = "/tmp/"

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
			'unit_id_0': Unit.unit_id.values().index("mole"),
			'unit_exponent_0': 1,
			'unit_scale_0': -9,
			'unit_multiplier_0': 1,
			'unit_id_1': Unit.unit_id.values().index("litre"),
			'unit_exponent_1': -1,
			'unit_scale_1': 1,
			'unit_multiplier_1': 1,
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
		json_response = loads(response_get_unit_definition.content)

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
