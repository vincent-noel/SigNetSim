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
		reaction = sbml_model.listOfReactions.getBySbmlId('reaction_2')


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
			'sbml_id': 'reaction_2'
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


		#
		# response_save_species = c.post('/edit/species/', {
		# 	'action': 'save',
		# 	'species_id': 2,
		# 	'species_name': "New name",
		# 	'species_sbml_id': "new_name",
		# 	'species_value': 75,
		# 	'species_value_type': 0,
		# 	'species_compartment': 0,
		# 	'species_unit': 2,
		# 	'species_constant': "on",
		# 	'species_boundary': "on",
		# })
		# 
		# self.assertEqual(response_save_species.status_code, 200)
		# 
		# sbml_doc = SbmlDocument()
		# sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		# sbml_model = sbml_doc.getModelInstance()
		# species = sbml_model.listOfSpecies.getBySbmlId('new_name')
		# 
		# self.assertTrue(species is not None)
		# self.assertEqual(species.getName(), "New name")
		# self.assertEqual(species.getValue(), 75)
		# self.assertEqual(species.hasOnlySubstanceUnits, True)
		# self.assertEqual(species.constant, True)
		# self.assertEqual(species.boundaryCondition, True)
		# 
		# response_delete_species = c.post('/edit/species/', {
		# 	'action': 'delete',
		# 	'species_id': sbml_model.listOfSpecies.values().index(species)
		# })
		# self.assertEqual(response_delete_species.status_code, 200)
		# self.assertEqual(response_delete_species.context['getErrors'], ['Species is used in reactions'])
		# 
		# response_save_new_species = c.post('/edit/species/', {
		# 	'action': 'save',
		# 	'species_id': "",
		# 	'species_name': "New species",
		# 	'species_sbml_id': "new_species",
		# 	'species_value': 2500,
		# 	'species_value_type': 0,
		# 	'species_compartment': 0,
		# 	'species_unit': 2,
		# 	'species_constant': "off",
		# 	'species_boundary': "off",
		# })
		# 
		# self.assertEqual(response_save_new_species.status_code, 200)
		# 
		# sbml_doc = SbmlDocument()
		# sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		# sbml_model = sbml_doc.getModelInstance()
		# species = sbml_model.listOfSpecies.getBySbmlId('new_species')
		# 
		# self.assertTrue(species != None)
		# self.assertEqual(species.getName(), "New species")
		# self.assertEqual(species.getValue(), 2500)
		# self.assertEqual(species.isConcentration(), False)
		# self.assertEqual(species.getCompartment().getName(), "cell")
		# self.assertEqual(species.constant, False)
		# self.assertEqual(species.boundaryCondition, False)
		# 
		# response_delete_species = c.post('/edit/species/', {
		# 	'action': 'delete',
		# 	'species_id': sbml_model.listOfSpecies.values().index(species)
		# })
		# self.assertEqual(response_delete_species.status_code, 200)
		# 
		# sbml_doc = SbmlDocument()
		# sbml_doc.readSbmlFromFile(join(settings.MEDIA_ROOT, str(model.sbml_file)))
		# sbml_model = sbml_doc.getModelInstance()
		# 
		# species = sbml_model.listOfSpecies.getBySbmlId('new_species')
		# 
		# self.assertEqual(species, None)

