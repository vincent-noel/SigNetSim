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

""" test_overview.py

	This file...

"""

from django.test import TestCase, Client
from django.conf import settings

from signetsim.models import User, Project, SbmlModel

from os.path import dirname, join
from json import loads


class TestOverview(TestCase):

	fixtures = ["user_with_project.json"]

	def testLoadGraph(self):

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

		response_choose_model = c.post('/edit/overview/', {
			'action': 'choose_model',
			'model_id': 3
		})
		self.assertEqual(response_choose_model.status_code, 200)
		self.assertEqual(
			[species.getSbmlId() for species in response_choose_model.context['list_of_species']],
			['sos', 'rasgtp', 'erkpp']
		)
		self.assertEqual(
			[reaction.getSbmlId() for reaction in response_choose_model.context['list_of_reactions']],
			[]
		)

		response_choose_submodel = c.post('/edit/overview/', {
			'action': 'choose_submodel',
			'submodel_id': 0
		})
		self.assertEqual(response_choose_submodel.status_code, 200)
		self.assertEqual(
			[species.getSbmlId() for species in response_choose_submodel.context['list_of_species']],
			['sos', 'rasgtp', 'erkpp']
		)
		self.assertEqual(
			[reaction.getSbmlId() for reaction in response_choose_submodel.context['list_of_reactions']],
			[]
		)

		response_choose_submodel = c.post('/edit/overview/', {
			'action': 'choose_submodel',
			'submodel_id': 1
		})
		self.assertEqual(response_choose_submodel.status_code, 200)

		self.assertEqual(
			[species.getSbmlId() for species in response_choose_submodel.context['list_of_species']],
			[
				'sos', 'rasgtp', 'erkpp', 'sos_mod__sos_i', 'sos_mod__fgf2', 'ras_mod__ras_gdp', 'ras_mod__sos_ras_gdp',
				'ras_mod__sos_ras_gtp', 'ras_mod__gap', 'ras_mod__gef', 'ras_mod__ras_n17', 'ras_mod__sos_ras_n17',
				'ras_mod__gef_rasn17', 'mapk_mod__raf', 'mapk_mod__raf_p', 'mapk_mod__mek', 'mapk_mod__mek_p',
				'mapk_mod__mek_pp', 'mapk_mod__mapk', 'mapk_mod__mapk_p'
			]
		)
		self.assertEqual(
			[reaction.getSbmlId() for reaction in response_choose_submodel.context['list_of_reactions']],
			['sos_mod__reaction_10', 'sos_mod__sos_inactivation_erk_pp', 'ras_mod__reaction_2', 'ras_mod__reaction_3',
			 'ras_mod__reaction_4', 'ras_mod__reaction_5', 'ras_mod__reaction_6', 'ras_mod__reaction_9',
			 'ras_mod__sosrasn17_comp', 'ras_mod__gefrasn17_comp', 'mapk_mod__Raf_activation_by_Ras_GTP',
			 'mapk_mod__Raf_inactivation', 'mapk_mod__Mek_activation_1', 'mapk_mod__Mek_activation_2',
			 'mapk_mod__Mek_inactivation_1', 'mapk_mod__Mek_inactivation_2', 'mapk_mod__Mapk_activation_1',
			 'mapk_mod__Mapk_activation_2', 'mapk_mod__Mapk_inactivation_1', 'mapk_mod__Mapk_inactivation_2',
			 'mapk_mod__RAF_inactivation_by_mapk']
		)

