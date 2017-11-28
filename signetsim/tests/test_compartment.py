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

""" test_compartment.py

	This file...

"""

from django.conf import settings
from django.test import TestCase, Client

from signetsim.models import User, Project, SbmlModel

from libsignetsim import SbmlDocument

from os.path import dirname, join
from json import loads


class TestCompartment(TestCase):

	fixtures = ["user_with_project.json"]

	def testCompartment(self):

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
		compartment = sbml_model.listOfCompartments.getBySbmlId('cell')

		response_get_compartment = c.post('/json/get_compartment/', {
			'sbml_id': 'cell',
		})

		self.assertEqual(response_get_compartment.status_code, 200)
		json_response = loads(response_get_compartment.content)

		self.assertEqual(json_response[u'id'], sbml_model.listOfCompartments.values().index(compartment))
		self.assertEqual(json_response[u'sbml_id'], compartment.getSbmlId())
		self.assertEqual(json_response[u'name'], compartment.getName())
		self.assertEqual(json_response[u'value'], compartment.getValue())
		self.assertEqual(json_response[u'constant'], 1 if compartment.constant else 0)

		response_choose_project = c.post('/models/', {
			'action': 'choose_project',
			'project_id': 0
		})
		self.assertEqual(response_choose_project.status_code, 200)
		self.assertEqual(response_choose_project.context['project_name'], "Project")

		response_choose_model = c.post('/edit/compartments/', {
			'action': 'choose_model',
			'model_id': 0
		})
		self.assertEqual(response_choose_model.status_code, 200)
		self.assertEqual(response_choose_model.context['model_name'], "SOS-Ras-MAPK with n17")

		response_save_compartment = c.post('/edit/compartments/', {
			'action': 'save',
			'compartment_id': sbml_model.listOfCompartments.values().index(compartment),
			'compartment_name': "New name",
			'compartment_sbml_id': "new_name",
			'compartment_size': 75,
			'compartment_unit': 2,
			'compartment_constant': "on",
			'compartment_sboterm': "",
		})

		self.assertEqual(response_save_compartment.status_code, 200)
		self.assertEqual(response_save_compartment.context['getErrors'], [])

		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		compartment = sbml_model.listOfCompartments.getBySbmlId('new_name')

		self.assertTrue(compartment is not None)
		self.assertEqual(compartment.getName(), "New name")
		self.assertEqual(compartment.getValue(), 75)
		self.assertEqual(compartment.constant, True)
		self.assertEqual(compartment.getUnits(), sbml_model.listOfUnitDefinitions[2])

		response_delete_compartment = c.post('/edit/compartments/', {
			'action': 'delete',
			'compartment_id': sbml_model.listOfCompartments.values().index(compartment)
		})
		self.assertEqual(response_delete_compartment.status_code, 200)
		self.assertEqual(response_delete_compartment.context['getErrors'], ['Compartment contains 25 species'])


		response_save_new_compartment = c.post('/edit/compartments/', {
			'action': 'save',
			'compartment_id': "",
			'compartment_name': "New compartment",
			'compartment_sbml_id': "new_compartment",
			'compartment_size': 75,
			'compartment_unit': "",
			'compartment_constant': "on",
			'compartment_sboterm': "",
		})

		self.assertEqual(response_save_new_compartment.status_code, 200)

		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		compartment = sbml_model.listOfCompartments.getBySbmlId('new_compartment')

		self.assertTrue(compartment != None)
		self.assertEqual(compartment.getName(), "New compartment")
		self.assertEqual(compartment.getValue(), 75)
		self.assertEqual(compartment.getUnits(), None)
		self.assertEqual(compartment.constant, True)


		response_delete_compartment = c.post('/edit/compartments/', {
			'action': 'delete',
			'compartment_id': sbml_model.listOfCompartments.values().index(compartment)
		})
		self.assertEqual(response_delete_compartment.status_code, 200)
		self.assertEqual(response_delete_compartment.context['getErrors'], [])
