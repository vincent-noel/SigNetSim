#!/usr/bin/env python
""" test_reactions.py


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
from libsignetsim.model.sbml.KineticLaw import KineticLaw
from os.path import dirname, join
from json import loads

class TestReactions(TestCase):

	fixtures = ["user_with_project.json"]

	def testReactions(self):

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
		reaction = sbml_model.listOfReactions.getBySbmlId('reaction_4')

		response_choose_project = c.post('/models/', {
			'action': 'choose_project',
			'project_id': 0
		})
		self.assertEqual(response_choose_project.status_code, 200)
		self.assertEqual(response_choose_project.context['project_name'], "Project")

		response_choose_model = c.post('/edit/reactions/', {
			'action': 'choose_model',
			'model_id': 0
		})
		self.assertEqual(response_choose_model.status_code, 200)
		self.assertEqual(response_choose_model.context['model_name'], "SOS-Ras-MAPK with n17")
		self.assertEqual(
			[t_reaction.getReactionDescription() for t_reaction in response_choose_model.context['list_of_reactions']],
			[t_reaction.getReactionDescription() for t_reaction in sbml_model.listOfReactions.values()]
		)


		response_get_reaction = c.post('/json/get_reaction/', {
			'sbml_id': 'reaction_4'
		})

		self.assertEqual(response_get_reaction.status_code, 200)
		json_response = loads(response_get_reaction.content)

		self.assertEqual(json_response[u'id'], sbml_model.listOfReactions.values().index(reaction))
		self.assertEqual(json_response[u'sbml_id'], reaction.getSbmlId())
		self.assertEqual(json_response[u'name'], reaction.getName())
		self.assertEqual(json_response[u'kinetic_law'], reaction.kineticLaw.getPrettyPrintMathFormula())
		self.assertEqual(json_response[u'reaction_type'], reaction.getReactionType())
		self.assertEqual(json_response[u'reaction_type_name'], KineticLaw.reactionTypes[reaction.getReactionType()])
		self.assertEqual(json_response[u'reversible'], reaction.reversible)

		self.assertEqual(json_response[u'list_of_reactants'], [
			[
				sbml_model.listOfSpecies.index(reactant.getSpecies()),
				reactant.stoichiometry.getPrettyPrintMathFormula()
			]
			for reactant in reaction.listOfReactants.values()
		])
		self.assertEqual(json_response[u'list_of_modifiers'], [
			[
				sbml_model.listOfSpecies.index(modifier.getSpecies()),
				modifier.stoichiometry.getPrettyPrintMathFormula()
			]
			for modifier in reaction.listOfModifiers.values()
		])
		self.assertEqual(json_response[u'list_of_products'], [
			[
				sbml_model.listOfSpecies.index(product.getSpecies()),
				product.stoichiometry.getPrettyPrintMathFormula()
			]
			for product in reaction.listOfProducts.values()
		])

		response_delete_reaction = c.post('/edit/reactions/', {
			'action': 'delete',
			'reaction_id': 2
		})

		self.assertEqual(response_delete_reaction.status_code, 200)

		model = SbmlModel.objects.filter(project=project)[0]
		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		self.assertEqual(len(sbml_model.listOfReactions), 21)
		self.assertEqual(sbml_model.listOfReactions.getBySbmlId('reaction_4'), None)
		response_create_creation = c.post('/edit/reactions/', {
			'action': 'save',
			'reaction_id': "",
			'reaction_sbml_id': "reaction_4",
			'reaction_name': "Ras activation by SOS-Ras-GDP",
			'reaction_reactant_0': 1,
			'reaction_reactant_0_stoichiometry': "1",
			'reaction_modifier_0': 3,
			'reaction_modifier_0_stoichiometry': "1",
			'reaction_product_0': 2,
			'reaction_product_0_stoichiometry': "1",
			'reaction_type': 1,
			'reaction_parameter_0': 2,
			'reaction_parameter_1': 3,
			'reaction_sboterm': ""
		})

		self.assertEqual(response_create_creation.status_code, 200)
		model = SbmlModel.objects.filter(project=project)[0]
		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		reaction = sbml_model.listOfReactions.getBySbmlId('reaction_4')
		self.assertEqual(len(sbml_model.listOfReactions), 22)
		self.assertEqual(reaction.getName(), "Ras activation by SOS-Ras-GDP")

		response_modify_creation = c.post('/edit/reactions/', {
			'action': 'save',
			'reaction_id': sbml_model.listOfReactions.values().index(reaction),
			'reaction_sbml_id': "reaction_4",
			'reaction_name': "Ras activation by SOS-Ras-GDP, modified",
			'reaction_reactant_0': 1,
			'reaction_reactant_0_stoichiometry': "1",
			'reaction_modifier_0': 3,
			'reaction_modifier_0_stoichiometry': "1",
			'reaction_product_0': 2,
			'reaction_product_0_stoichiometry': "1",
			'reaction_type': 1,
			'reaction_parameter_0': 2,
			'reaction_parameter_1': 3,
			'reaction_sboterm': ""
		})

		self.assertEqual(response_modify_creation.status_code, 200)
		model = SbmlModel.objects.filter(project=project)[0]
		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		sbml_model = sbml_doc.getModelInstance()
		reaction = sbml_model.listOfReactions.getBySbmlId('reaction_4')
		self.assertEqual(len(sbml_model.listOfReactions), 22)
		self.assertEqual(reaction.getName(), "Ras activation by SOS-Ras-GDP, modified")

