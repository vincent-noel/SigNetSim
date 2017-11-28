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

""" test_rule.py

	This file...

"""

from django.conf import settings
from django.test import TestCase, Client

from signetsim.models import User, Project, SbmlModel

from libsignetsim import SbmlDocument, MathFormula

from os.path import dirname, join
from json import loads
from sympy import simplify

class TestRule(TestCase):

	fixtures = ["user_with_project.json"]

	def testRule(self):

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
		listOfRules = sbml_model.listOfRules.values() + sbml_model.listOfInitialAssignments.values()
		listOfVariables = []
		for variable in sbml_model.listOfVariables.values():
			if ((variable.isParameter() and variable.isGlobal())
				or variable.isSpecies()
				or variable.isCompartment()
				or variable.isStoichiometry()):
				listOfVariables.append(variable)

		rule = listOfRules[0]

		response_get_compartment = c.post('/json/get_rule/', {
			'rule_ind': '0',
		})

		self.assertEqual(response_get_compartment.status_code, 200)
		json_response = loads(response_get_compartment.content)


		self.assertEqual(json_response[u'rule_id'], listOfRules.index(rule))
		self.assertEqual(json_response[u'rule_type'], 1)
		self.assertEqual(json_response[u'variable'], listOfVariables.index(sbml_model.listOfVariables.getBySbmlId('total_ras_gtp')))

		response_choose_project = c.post('/models/', {
			'action': 'choose_project',
			'project_id': 0
		})
		self.assertEqual(response_choose_project.status_code, 200)
		self.assertEqual(response_choose_project.context['project_name'], "Project")

		response_choose_model = c.post('/edit/rules/', {
			'action': 'choose_model',
			'model_id': 0
		})
		self.assertEqual(response_choose_model.status_code, 200)
		self.assertEqual(response_choose_model.context['model_name'], "SOS-Ras-MAPK with n17")

		response_save_rule = c.post('/edit/rules/', {
			'action': 'save',
			'rule_id': listOfRules.index(rule),
			'rule_type': 1,
			'variable_id': listOfVariables.index(sbml_model.listOfVariables.getBySbmlId('total_mapk_activated')),
			'rule_expression': "75*ras_gtp",
		})

		self.assertEqual(response_save_rule.status_code, 200)
		self.assertEqual(response_save_rule.context['form'].getErrors(), [])

		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		listOfRules = sbml_model.listOfRules.values() + sbml_model.listOfInitialAssignments.values()
		listOfVariables = []
		for variable in sbml_model.listOfVariables.values():
			if ((variable.isParameter() and variable.isGlobal())
				or variable.isSpecies()
				or variable.isCompartment()
				or variable.isStoichiometry()):
				listOfVariables.append(variable)

		rule = listOfRules[0]


		self.assertEqual(rule.getType(), 1)
		self.assertEqual(rule.getVariable(), sbml_model.listOfVariables.getBySbmlId('total_mapk_activated'))
		formula = MathFormula(sbml_model)
		formula.setPrettyPrintMathFormula("75*ras_gtp", rawFormula=True)
		self.assertEqual(simplify(rule.getDefinition().getDeveloppedInternalMathFormula()-formula.getDeveloppedInternalMathFormula()), 0)

		response_delete_rule = c.post('/edit/rules/', {
			'action': 'delete',
			'rule_id': 0
		})
		self.assertEqual(response_delete_rule.status_code, 200)
		self.assertEqual(response_delete_rule.context['form'].getErrors(), [])
