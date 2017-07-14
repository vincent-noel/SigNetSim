#!/usr/bin/env python
""" test_model.py


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

from django.test import TestCase, Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from signetsim.models import User, Project, SbmlModel
from signetsim.views.ListOfModelsView import ListOfModelsView
from django.conf import settings
from os.path import dirname, join
from shutil import rmtree

class TestSelectSubmodel(TestCase):

	fixtures = ["user_with_project.json"]

	def testCreateModel(self):

		settings.MEDIA_ROOT = "/tmp/"

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

		response_choose_model = c.post('/edit/species/', {
			'action': 'choose_model',
			'model_id': 0
		})
		self.assertEqual(response_choose_model.status_code, 200)
		self.assertEqual(
			[sbml_model.name for sbml_model in response_choose_model.context['sbml_models']],
			[u'SOS', u'Ras', u'MAPK', u'SOS-Ras-MAPK']
		)
		self.assertEqual(
			[submodel for submodel in response_choose_model.context['model_submodels']],
			['Model definition']
		)

		self.assertEqual(
			[species.getNameOrSbmlId() for species in response_choose_model.context['list_of_species']],
			['SOS', 'SOS_inactive', 'FGF2', 'ERK-PP']
		)

		response_choose_model = c.post('/edit/species/', {
			'action': 'choose_model',
			'model_id': 1
		})
		self.assertEqual(response_choose_model.status_code, 200)
		self.assertEqual(
			[sbml_model.name for sbml_model in response_choose_model.context['sbml_models']],
			[u'SOS', u'Ras', u'MAPK', u'SOS-Ras-MAPK']
		)
		self.assertEqual(
			[submodel for submodel in response_choose_model.context['model_submodels']],
			['Model definition']
		)

		self.assertEqual(
			[species.getNameOrSbmlId() for species in response_choose_model.context['list_of_species']],
			[
				'SOS', 'Ras-GDP', 'Ras-GTP', 'SOS-Ras-GDP', 'SOS-Ras-GTP',
				'GAP', 'GEF', 'Ras-N17', 'SOS-Ras-N17', 'GEF-RasN17'
			]
		)

		response_choose_model = c.post('/edit/species/', {
			'action': 'choose_model',
			'model_id': 2
		})

		self.assertEqual(response_choose_model.status_code, 200)
		self.assertEqual(
			[sbml_model.name for sbml_model in response_choose_model.context['sbml_models']],
			[u'SOS', u'Ras', u'MAPK', u'SOS-Ras-MAPK']
		)
		self.assertEqual(
			[submodel for submodel in response_choose_model.context['model_submodels']],
			['Model definition']
		)

		self.assertEqual(
			[species.getNameOrSbmlId() for species in response_choose_model.context['list_of_species']],
			[
				'Ras-GTP', 'Raf', 'Raf-P', 'Mek', 'Mek-P', 'Mek-PP',
				'Mapk', 'Mapk-P', 'Mapk-PP', 'Total MEK activated', 'Total MAPK activated'
			]
		)

		response_choose_model = c.post('/edit/species/', {
			'action': 'choose_model',
			'model_id': 3
		})
		self.assertEqual(response_choose_model.status_code, 200)
		self.assertEqual(
			[sbml_model.name for sbml_model in response_choose_model.context['sbml_models']],
			[u'SOS', u'Ras', u'MAPK', u'SOS-Ras-MAPK']
		)
		self.assertEqual(
			[submodel for submodel in response_choose_model.context['model_submodels']],
			['Model definition']
		)

		self.assertEqual(
			[species.getNameOrSbmlId() for species in response_choose_model.context['list_of_species']],
			['SOS', 'Ras-GTP', 'ERK-PP']
		)


		response_choose_submodel = c.post('/edit/species/', {
			'action': 'choose_submodel',
			'submodel_id': 0
		})
		self.assertEqual(response_choose_submodel.status_code, 200)
		self.assertEqual(
			[species.getNameOrSbmlId() for species in response_choose_submodel.context['list_of_species']],
			['SOS', 'Ras-GTP', 'ERK-PP']
		)

		response_choose_submodel = c.post('/edit/species/', {
			'action': 'choose_submodel',
			'submodel_id': 1
		})
		self.assertEqual(response_choose_submodel.status_code, 200)
		self.assertEqual(
			[species.getNameOrSbmlId() for species in response_choose_submodel.context['list_of_species']],
			['SOS', 'SOS_inactive', 'FGF2', 'ERK-PP']
		)

		response_choose_submodel = c.post('/edit/species/', {
			'action': 'choose_submodel',
			'submodel_id': 2
		})

		self.assertEqual(response_choose_submodel.status_code, 200)
		self.assertEqual(
			[species.getNameOrSbmlId() for species in response_choose_submodel.context['list_of_species']],
			['SOS', 'Ras-GTP', 'ERK-PP', 'SOS_inactive', 'FGF2', 'Ras-GDP', 'SOS-Ras-GDP', 'SOS-Ras-GTP', 'GAP', 'GEF',
			 'Ras-N17', 'SOS-Ras-N17', 'GEF-RasN17', 'SOS-Ras-GTP', 'Raf', 'Raf-P', 'Mek', 'Mek-P', 'Mek-PP', 'Mapk',
			 'Mapk-P', 'Total MEK activated', 'Total MAPK activated']
		)
