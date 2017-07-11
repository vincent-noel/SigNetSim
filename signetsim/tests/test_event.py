#!/usr/bin/env python
""" test_parameter.py


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
from signetsim.views.ListOfModelsView import ListOfModelsView

from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.model.math.MathFormula import MathFormula

from os.path import dirname, join
from json import loads
from sympy import simplify

class TestEvent(TestCase):

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
		listOfVariables = []
		for variable in sbml_model.listOfVariables.values():
			if ((variable.isParameter() and variable.isGlobal())
				or variable.isSpecies()
				or variable.isCompartment()
				or variable.isStoichiometry()):
				listOfVariables.append(variable)

		response_choose_project = c.post('/models/', {
			'action': 'choose_project',
			'project_id': 0
		})
		self.assertEqual(response_choose_project.status_code, 200)
		self.assertEqual(response_choose_project.context['project_name'], "Project")

		response_choose_model = c.post('/edit/events/', {
			'action': 'choose_model',
			'model_id': 0
		})
		self.assertEqual(response_choose_model.status_code, 200)
		self.assertEqual(response_choose_model.context['model_name'], "SOS-Ras-MAPK with n17")

		response_save_event = c.post('/edit/events/', {
			'action': 'save',
			'event_id': '',
			'event_name': "Test event",
			'event_trigger': "time==0",
			'event_priority': "",
			'event_delay': "",
			'event_assignment_0_id': listOfVariables.index(sbml_model.listOfVariables.getBySbmlId('ras_gtp')),
			'event_assignment_0_expression': 'ras_gtp*2'
		})

		self.assertEqual(response_save_event.status_code, 200)
		self.assertEqual(response_save_event.context['form'].getErrors(), [])

		model = SbmlModel.objects.filter(project=project)[0]
		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		listOfVariables = []
		for variable in sbml_model.listOfVariables.values():
			if ((variable.isParameter() and variable.isGlobal())
				or variable.isSpecies()
				or variable.isCompartment()
				or variable.isStoichiometry()):
				listOfVariables.append(variable)

		response_get_event = c.post('/json/get_event/', {
			'event_ind': '0',
		})

		self.assertEqual(response_get_event.status_code, 200)
		json_response = loads(response_get_event.content)


		self.assertEqual(json_response[u'event_ind'], 0)
		self.assertEqual(json_response[u'event_name'], "Test event")

		formula = MathFormula(sbml_model)
		formula.setPrettyPrintMathFormula("time==0", rawFormula=True)

		formula_response = MathFormula(sbml_model)
		formula_response.setPrettyPrintMathFormula(json_response[u'event_trigger'], rawFormula=True)

		self.assertEqual(simplify(formula.getDeveloppedInternalMathFormula()-formula_response.getDeveloppedInternalMathFormula()), 0)
		self.assertEqual(json_response[u'event_delay'], "")
		self.assertEqual(json_response[u'event_assignment_variable_0'], listOfVariables.index(sbml_model.listOfVariables.getBySbmlId('ras_gtp')))

		formula = MathFormula(sbml_model)
		formula.setPrettyPrintMathFormula("ras_gtp*2", rawFormula=True)

		formula_response = MathFormula(sbml_model)
		formula_response.setPrettyPrintMathFormula(json_response[u'event_assignment_definition_0'], rawFormula=True)
		self.assertEqual(simplify(formula.getDeveloppedInternalMathFormula()-formula_response.getDeveloppedInternalMathFormula()), 0)
		self.assertTrue(u'event_assignment_variable_1' not in json_response)

		# Modifying an event
		response_save_event = c.post('/edit/events/', {
			'action': 'save',
			'event_id': '0',
			'event_name': "Test event",
			'event_trigger': "time==100",
			'event_priority': "",
			'event_delay': "",
			'event_assignment_0_id': listOfVariables.index(sbml_model.listOfVariables.getBySbmlId('ras_gtp')),
			'event_assignment_0_expression': 'ras_gtp*2',
			'event_assignment_1_id': listOfVariables.index(sbml_model.listOfVariables.getBySbmlId('ras_gdp')),
			'event_assignment_1_expression': 'ras_gdp/2',

		})
		self.assertEqual(response_save_event.status_code, 200)
		self.assertEqual(response_save_event.context['form'].getErrors(), [])

		model = SbmlModel.objects.filter(project=project)[0]
		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		event = sbml_model.listOfEvents.values()[0]
		listOfVariables = []
		for variable in sbml_model.listOfVariables.values():
			if ((variable.isParameter() and variable.isGlobal())
				or variable.isSpecies()
				or variable.isCompartment()
				or variable.isStoichiometry()):
				listOfVariables.append(variable)

		self.assertEqual(event.getNameOrSbmlId(), "Test event")

		formula = MathFormula(sbml_model)
		formula.setPrettyPrintMathFormula("time==100", rawFormula=True)

		self.assertEqual(
			simplify(formula.getDeveloppedInternalMathFormula() - event.trigger.getDeveloppedInternalMathFormula()),
			0)

		self.assertEqual(event.priority, None)
		self.assertEqual(event.delay, None)
		self.assertEqual(event.listOfEventAssignments[0].getVariable(), sbml_model.listOfVariables.getBySbmlId('ras_gtp'))

		formula = MathFormula(sbml_model)
		formula.setPrettyPrintMathFormula("ras_gtp*2")

		self.assertEqual(
			simplify(formula.getDeveloppedInternalMathFormula() - event.listOfEventAssignments[0].getDefinition().getDeveloppedInternalMathFormula()),
			0)

		self.assertEqual(event.listOfEventAssignments[1].getVariable(), sbml_model.listOfVariables.getBySbmlId('ras_gdp'))

		formula = MathFormula(sbml_model)
		formula.setPrettyPrintMathFormula("ras_gdp/2")

		self.assertEqual(
			simplify(formula.getDeveloppedInternalMathFormula() - event.listOfEventAssignments[1].getDefinition().getDeveloppedInternalMathFormula()),
			0)


		response_delete_event = c.post('/edit/events/', {
			'action': 'delete',
			'event_id': 0
		})
		self.assertEqual(response_delete_event.status_code, 200)
		self.assertEqual(response_delete_event.context['form'].getErrors(), [])
		self.assertEqual(json_response[u'event_ind'], 0)
		self.assertEqual(json_response[u'event_name'], "Test event")
		self.assertEqual(json_response[u'event_trigger'], "time == 0")
		self.assertEqual(json_response[u'event_priority'], "")
		self.assertEqual(json_response[u'event_delay'], "")


		model = SbmlModel.objects.filter(project=project)[0]
		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		self.assertEqual(len(sbml_model.listOfEvents), 0)

