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

""" test_species.py

	This file...

"""

from django.conf import settings
from django.test import TestCase, Client

from signetsim.models import User, Project, SbmlModel
from signetsim.views.ListOfModelsView import ListOfModelsView

from libsignetsim.model.SbmlDocument import SbmlDocument

from os.path import dirname, join
from json import loads

class TestSpecies(TestCase):

	fixtures = ["user_with_project.json"]

	def testSpecies(self):

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
		species = sbml_model.listOfSpecies.getBySbmlId('ras_gtp')

		response_get_species = c.post('/json/get_species/', {
			'sbml_id': 'ras_gtp'
		})

		self.assertEqual(response_get_species.status_code, 200)
		json_response = loads(response_get_species.content)
		self.assertEqual(json_response[u'id'], sbml_model.listOfSpecies.values().index(species))
		self.assertEqual(json_response[u'sbml_id'], species.getSbmlId())
		self.assertEqual(json_response[u'name'], species.getName())
		self.assertEqual(json_response[u'compartment_name'], species.getCompartment().getName())
		self.assertEqual(json_response[u'compartment_id'], sbml_model.listOfCompartments.values().index(species.getCompartment()))
		self.assertEqual(json_response[u'value'], species.getValue())
		self.assertEqual(json_response[u'isConcentration'], 1 if not species.hasOnlySubstanceUnits else 0)
		self.assertEqual(json_response[u'constant'], 1 if species.constant else 0)
		self.assertEqual(json_response[u'boundaryCondition'], 1 if species.boundaryCondition else 0)


		response_choose_project = c.post('/models/', {
			'action': 'choose_project',
			'project_id': 0
		})
		self.assertEqual(response_choose_project.status_code, 200)
		self.assertEqual(response_choose_project.context['project_name'], "Project")

		response_choose_model = c.post('/edit/species/', {
			'action': 'choose_model',
			'model_id': 0
		})
		self.assertEqual(response_choose_model.status_code, 200)
		self.assertEqual(response_choose_model.context['model_name'], "SOS-Ras-MAPK with n17")

		response_save_species = c.post('/edit/species/', {
			'action': 'save',
			'species_id': 2,
			'species_name': "New name",
			'species_sbml_id': "new_name",
			'species_value': 75,
			'species_value_type': 0,
			'species_compartment': 0,
			'species_unit': 2,
			'species_constant': "on",
			'species_boundary': "on",
			'species_sboterm': "",
		})

		self.assertEqual(response_save_species.status_code, 200)

		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		species = sbml_model.listOfSpecies.getBySbmlId('new_name')

		self.assertTrue(species is not None)
		self.assertEqual(species.getName(), "New name")
		self.assertEqual(species.getValue(), 75)
		self.assertEqual(species.hasOnlySubstanceUnits, True)
		self.assertEqual(species.constant, True)
		self.assertEqual(species.boundaryCondition, True)

		response_delete_species = c.post('/edit/species/', {
			'action': 'delete',
			'species_id': sbml_model.listOfSpecies.values().index(species)
		})
		self.assertEqual(response_delete_species.status_code, 200)
		self.assertEqual(response_delete_species.context['getErrors'], ['Species is used in reactions'])

		response_save_new_species = c.post('/edit/species/', {
			'action': 'save',
			'species_id': "",
			'species_name': "New species",
			'species_sbml_id': "new_species",
			'species_value': 2500,
			'species_value_type': 0,
			'species_compartment': 0,
			'species_unit': 2,
			'species_constant': "off",
			'species_boundary': "off",
			'species_sboterm': "",
		})

		self.assertEqual(response_save_new_species.status_code, 200)

		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		species = sbml_model.listOfSpecies.getBySbmlId('new_species')

		self.assertTrue(species != None)
		self.assertEqual(species.getName(), "New species")
		self.assertEqual(species.getValue(), 2500)
		self.assertEqual(species.isConcentration(), False)
		self.assertEqual(species.getCompartment().getName(), "cell")
		self.assertEqual(species.constant, False)
		self.assertEqual(species.boundaryCondition, False)

		response_delete_species = c.post('/edit/species/', {
			'action': 'delete',
			'species_id': sbml_model.listOfSpecies.values().index(species)
		})
		self.assertEqual(response_delete_species.status_code, 200)

		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()

		species = sbml_model.listOfSpecies.getBySbmlId('new_species')

		self.assertEqual(species, None)