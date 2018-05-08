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

""" test_parameter.py

	This file...

"""

from django.conf import settings
from django.test import TestCase, Client

from signetsim.models import User, Project, SbmlModel

from libsignetsim import SbmlDocument

from os.path import dirname, join
from json import loads


class TestParameter(TestCase):

	fixtures = ["user_with_project.json"]

	def testGlobalParameter(self):

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
		parameter = sbml_model.listOfParameters.getBySbmlId('sos_ras_gdp_comp')

		response_get_parameter = c.post('/json/get_parameter/', {
			'sbml_id': 'sos_ras_gdp_comp',
			'reaction': ''
		})

		self.assertEqual(response_get_parameter.status_code, 200)
		json_response = loads(response_get_parameter.content.decode('utf-8'))
		self.assertEqual(json_response[u'id'], sbml_model.listOfParameters.index(parameter))
		self.assertEqual(json_response[u'sbml_id'], parameter.getSbmlId())
		self.assertEqual(json_response[u'name'], parameter.getName())
		self.assertEqual(json_response[u'value'], parameter.getValue())
		self.assertEqual(json_response[u'constant'], 1 if parameter.constant else 0)

		response_choose_project = c.post('/models/', {
			'action': 'choose_project',
			'project_id': 0
		})
		self.assertEqual(response_choose_project.status_code, 200)
		self.assertEqual(response_choose_project.context['project_name'], "Project")

		response_choose_model = c.post('/edit/parameters/', {
			'action': 'choose_model',
			'model_id': 0
		})
		self.assertEqual(response_choose_model.status_code, 200)
		self.assertEqual(response_choose_model.context['model_name'], "SOS-Ras-MAPK with n17")

		response_save_parameter = c.post('/edit/parameters/', {
			'action': 'save',
			'parameter_id': sbml_model.listOfParameters.index(parameter),
			'parameter_name': "New name",
			'parameter_sbml_id': "new_name",
			'parameter_value': 75,
			'parameter_unit': 2,
			'parameter_constant': "on",
			'parameter_scope': 0,
			'parameter_sboterm': "",
		})

		self.assertEqual(response_save_parameter.status_code, 200)
		self.assertEqual(response_save_parameter.context['getErrors'], [])

		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		parameter = sbml_model.listOfParameters.getBySbmlId('new_name')

		self.assertTrue(parameter is not None)
		self.assertEqual(parameter.getName(), "New name")
		self.assertEqual(parameter.getValue(), 75)
		self.assertEqual(parameter.constant, True)
		self.assertEqual(parameter.getUnits(), sbml_model.listOfUnitDefinitions[2])

		response_delete_parameter = c.post('/edit/parameters/', {
			'action': 'delete',
			'parameter_id': sbml_model.listOfParameters.index(parameter)
		})
		self.assertEqual(response_delete_parameter.status_code, 200)
		self.assertEqual(response_delete_parameter.context['getErrors'], ['Parameter in used in reactions'])


		response_save_new_parameter = c.post('/edit/parameters/', {
			'action': 'save',
			'parameter_id': "",
			'parameter_name': "New parameter",
			'parameter_sbml_id': "new_parameter",
			'parameter_value': 75,
			'parameter_unit': 2,
			'parameter_constant': "",
			'parameter_scope': 0,
			'parameter_sboterm': "",
		})

		self.assertEqual(response_save_new_parameter.status_code, 200)

		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		parameter = sbml_model.listOfParameters.getBySbmlId('new_parameter')

		self.assertTrue(parameter != None)
		self.assertEqual(parameter.getName(), "New parameter")
		self.assertEqual(parameter.getValue(), 75)
		self.assertEqual(parameter.getUnits(), sbml_model.listOfUnitDefinitions[2])
		self.assertEqual(parameter.constant, False)

		response_delete_parameter = c.post('/edit/parameters/', {
			'action': 'delete',
			'parameter_id': sbml_model.listOfParameters.index(parameter)
		})
		self.assertEqual(response_delete_parameter.status_code, 200)
		self.assertEqual(response_delete_parameter.context['getErrors'], [])


	def testLocalParameter(self):

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
		parameter = sbml_model.listOfParameters.getBySbmlId('sos_ras_gdp_comp')

		response_get_reaction = c.post('/json/get_reaction/', {
			'sbml_id': 'reaction_2',
		})

		self.assertEqual(response_get_reaction.status_code, 200)
		json_response = loads(response_get_reaction.content.decode('utf-8'))
		self.assertEqual(json_response[u'kinetic_law'], '-1 * sos_ras_gdp * sos_ras_gdp_decomp + ras_gdp * sos * sos_ras_gdp_comp')

		response_get_parameter = c.post('/json/get_parameter/', {
			'sbml_id': 'sos_ras_gdp_comp',
			'reaction': ''
		})

		self.assertEqual(response_get_parameter.status_code, 200)
		json_response = loads(response_get_parameter.content.decode('utf-8'))
		self.assertEqual(json_response[u'id'], sbml_model.listOfParameters.index(parameter))
		self.assertEqual(json_response[u'reaction_id'], "")

		response_to_local_parameter = c.post('/edit/parameters/', {
			'action': 'save',
			'parameter_id': json_response[u'id'],
			'parameter_name': json_response[u'name'],
			'parameter_sbml_id': json_response[u'sbml_id'],
			'parameter_value': json_response[u'value'],
			'parameter_unit': json_response[u'unit_id'],
			'parameter_constant': "on" if json_response[u'constant'] == 1 else "",
			'parameter_scope': 1,
			'parameter_sboterm': "",
		})

		self.assertEqual(response_to_local_parameter.status_code, 200)
		self.assertEqual(response_to_local_parameter.context['getErrors'], [])
		self.assertEqual(response_to_local_parameter.context['form'].getErrors(), [])

		response_get_reaction = c.post('/json/get_reaction/', {
			'sbml_id': 'reaction_2',
		})

		self.assertEqual(response_get_reaction.status_code, 200)
		json_response = loads(response_get_reaction.content.decode('utf-8'))
		self.assertEqual(
			json_response[u'kinetic_law'],
			'-1 * sos_ras_gdp * sos_ras_gdp_decomp + sos_ras_gdp_comp * ras_gdp * sos'
		)

		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		reaction = sbml_model.listOfReactions.getBySbmlId('reaction_2')
		self.assertEqual(
			str(reaction.kineticLaw.getDefinition().getInternalMathFormula()),
			"_local_0_sos_ras_gdp_comp*ras_gdp*sos - sos_ras_gdp*sos_ras_gdp_decomp"
		)

		self.assertEqual(sbml_model.listOfParameters.getBySbmlId("sos_ras_gdp_comp"), None)

		response_get_parameter = c.post('/json/get_parameter/', {
			'sbml_id': 'sos_ras_gdp_comp',
			'reaction': '1'
		})

		self.assertEqual(response_get_parameter.status_code, 200)
		json_response = loads(response_get_parameter.content.decode('utf-8'))

		response_list_parameters = c.get('/edit/parameters/')
		self.assertEqual(response_list_parameters.status_code, 200)
		list_of_parameters = [param.getSbmlId() for param in response_list_parameters.context['list_of_parameters']]



		response_to_global_parameter = c.post('/edit/parameters/', {
			'action': 'save',
			'parameter_id': list_of_parameters.index("sos_ras_gdp_comp"),
			'parameter_name': json_response[u'name'],
			'parameter_sbml_id': json_response[u'sbml_id'],
			'parameter_value': json_response[u'value'],
			'parameter_unit': json_response[u'unit_id'],
			'parameter_constant': "on" if json_response[u'constant'] == 1 else "",
			'parameter_scope': 0,
			'parameter_sboterm': "",
		})

		self.assertEqual(response_to_global_parameter.status_code, 200)
		self.assertEqual(response_to_global_parameter.context['getErrors'], [])
		self.assertEqual(response_to_global_parameter.context['form'].getErrors(), [])

		response_get_reaction = c.post('/json/get_reaction/', {
			'sbml_id': 'reaction_2',
		})

		self.assertEqual(response_get_reaction.status_code, 200)
		json_response = loads(response_get_reaction.content.decode('utf-8'))
		# print json_response
		self.assertEqual(
			json_response[u'kinetic_law'],
			'-1 * sos_ras_gdp * sos_ras_gdp_decomp + ras_gdp * sos * sos_ras_gdp_comp'
		)

		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		reaction = sbml_model.listOfReactions.getBySbmlId('reaction_2')
		self.assertEqual(
			str(reaction.kineticLaw.getDefinition().getInternalMathFormula()),
			"ras_gdp*sos*sos_ras_gdp_comp - sos_ras_gdp*sos_ras_gdp_decomp"
		)

		self.assertEqual(sbml_model.listOfParameters.getBySbmlId("sos_ras_gdp_comp").getSbmlId(), "sos_ras_gdp_comp")