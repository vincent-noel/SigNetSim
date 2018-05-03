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

""" test_public.py

	This file tests the access control of projects 

"""

from django.test import TestCase, Client
from django.conf import settings

from signetsim.models import User, Project, SbmlModel, Experiment, Condition, SEDMLSimulation

class TestPublicAccess(TestCase):

	fixtures = ["users.json"]

	def test_public_access(self):

		user = User.objects.filter(username='test_user')
		self.assertTrue(not Project.objects.filter(user=user).exists())

		c_loggedin = Client()
		self.assertTrue(c_loggedin.login(username='test_user', password='password'))

		# Private

		response_create_project = c_loggedin.post('/', {
			'action': 'save_project',
			'modal_project_name': 'Private project'
		})

		self.assertEqual(response_create_project.status_code, 200)
		self.assertEqual(len(Project.objects.filter(user=user)), 1)

		private_project = Project.objects.filter(user=user)[0]

		self.assertEqual(private_project.name, "Private project")

		response_choose_project = c_loggedin.get('/project/%s/' % private_project.folder)
		self.assertEqual(response_choose_project.status_code, 302)

		response_new_model = c_loggedin.post('/models/', {
			'action': 'new_model',
			'model_name': 'Model private'
		})

		self.assertEqual(response_new_model.status_code, 200)
		private_model = SbmlModel.objects.filter(project=private_project)[0]


		response_choose_model = c_loggedin.post('/edit/species/', {
			'action': 'choose_model',
			'model_id': 0
		})
		self.assertEqual(response_choose_model.status_code, 200)

		response_new_species = c_loggedin.post('/edit/species/', {
			'action': 'save',
			'species_id': "",
			'species_name': "New name",
			'species_sbml_id': "new_name",
			'species_value': 75,
			'species_value_type': 0,
			'species_compartment': 0,
			'species_unit': 2,
			'species_constant': "",
			'species_boundary': "on",
			'species_sboterm': "",
		})
		self.assertEqual(response_new_species.status_code, 200)

		response_new_experiment = c_loggedin.post('/data/', {
			'action': 'save',
			'experiment_id': "",
			'experiment_name': "Private experiment",
			'experiment_notes': ""
		})

		self.assertEqual(response_new_experiment.status_code, 200)
		private_data = Experiment.objects.filter(project=private_project)[0]

		response_new_condition = c_loggedin.post('/data/%d/' % private_data.id, {
			'action': 'save',
			'condition_id': "",
			'condition_name': "Private condition",
			'condition_notes': "Some notes"
		})
		self.assertEqual(response_new_condition.status_code, 200)
		private_condition = Condition.objects.filter(experiment=private_data)[0]

		response_simulate_model = c_loggedin.post('/simulate/timeseries/', {
			'action': 'simulate_model',
			'species_selected': [0],
			'experiment_id': "",
			'time_min': 0,
			'time_ech': 60,
			'time_max': 3600
		})

		self.assertEqual(response_simulate_model.status_code, 200)
		self.assertEqual(response_simulate_model.context['form'].getErrors(), [])

		self.assertEqual(len(SEDMLSimulation.objects.filter(project=private_project)), 0)
		response_save_simulation = c_loggedin.post('/simulate/timeseries/', {
			'action': 'save_simulation',
			'species_selected': [0],
			'experiment_id': "",
			'time_min': 0,
			'time_ech': 60,
			'time_max': 3600
		})

		self.assertEqual(response_save_simulation.status_code, 200)
		self.assertEqual(response_save_simulation.context['form'].getErrors(), [])
		self.assertEqual(len(SEDMLSimulation.objects.filter(project=private_project)), 1)

		private_simulation = SEDMLSimulation.objects.filter(project=private_project)[0]

		# Public

		response_create_project = c_loggedin.post('/', {
			'action': 'save_project',
			'modal_project_access': 'on',
			'modal_project_name': 'Public project'
		})

		self.assertEqual(response_create_project.status_code, 200)
		self.assertEqual(len(Project.objects.filter(user=user)), 2)

		public_project = Project.objects.filter(user=user)[1]

		self.assertEqual(public_project.name, "Public project")

		response_choose_project = c_loggedin.get('/project/%s/' % public_project.folder)
		self.assertEqual(response_choose_project.status_code, 302)

		response_new_model = c_loggedin.post('/models/', {
			'action': 'new_model',
			'model_name': 'Model public'
		})
		self.assertEqual(response_new_model.status_code, 200)
		public_model = SbmlModel.objects.filter(project=public_project)[0]
		response_choose_model = c_loggedin.post('/edit/species/', {
			'action': 'choose_model',
			'model_id': 0
		})
		self.assertEqual(response_choose_model.status_code, 200)

		response_new_species = c_loggedin.post('/edit/species/', {
			'action': 'save',
			'species_id': "",
			'species_name': "New name",
			'species_sbml_id': "new_name",
			'species_value': 75,
			'species_value_type': 0,
			'species_compartment': 0,
			'species_unit': 2,
			'species_constant': "",
			'species_boundary': "on",
			'species_sboterm': "",
		})
		self.assertEqual(response_new_species.status_code, 200)

		response_new_experiment = c_loggedin.post('/data/', {
			'action': 'save',
			'experiment_id': "",
			'experiment_name': "Public experiment",
			'experiment_notes': ""
		})
		self.assertEqual(response_new_experiment.status_code, 200)
		public_data = Experiment.objects.filter(project=public_project)[0]

		response_new_condition = c_loggedin.post('/data/%d/' % public_data.id, {
			'action': 'save',
			'condition_id': "",
			'condition_name': "Public condition",
			'condition_notes': "Some notes"
		})
		self.assertEqual(response_new_condition.status_code, 200)
		public_condition = Condition.objects.filter(experiment=public_data)[0]

		response_simulate_model = c_loggedin.post('/simulate/timeseries/', {
			'action': 'simulate_model',
			'species_selected': [0],
			'experiment_id': "",
			'time_min': 0,
			'time_ech': 60,
			'time_max': 3600
		})

		self.assertEqual(response_simulate_model.status_code, 200)
		self.assertEqual(response_simulate_model.context['form'].getErrors(), [])

		self.assertEqual(len(SEDMLSimulation.objects.filter(project=public_project)), 0)
		response_save_simulation = c_loggedin.post('/simulate/timeseries/', {
			'action': 'save_simulation',
			'species_selected': [0],
			'experiment_id': "",
			'time_min': 0,
			'time_ech': 60,
			'time_max': 3600
		})

		self.assertEqual(response_save_simulation.status_code, 200)
		self.assertEqual(response_save_simulation.context['form'].getErrors(), [])
		self.assertEqual(len(SEDMLSimulation.objects.filter(project=public_project)), 1)

		public_simulation = SEDMLSimulation.objects.filter(project=public_project)[0]

		c_guest = Client()

		response_list_projects = c_guest.get('/')

		self.assertEqual(response_list_projects.status_code, 200)
		self.assertEqual(len(response_list_projects.context['projects']), 1)
		self.assertEqual(response_list_projects.context['projects'][0].name, "Public project")


		response_get_public = c_guest.get('/project/%s/' % str(public_project.folder))
		self.assertEqual(response_get_public.status_code, 302)

		response_get_public_model = c_guest.get('/edit/model/%d/' % public_model.id)
		self.assertEqual(response_get_public_model.status_code, 302)

		response_get_public_data = c_guest.get('/data/%d/' % public_data.id)
		self.assertEqual(response_get_public_data.status_code, 200)

		response_get_public_condition = c_guest.get('/data/%d/%d/' % (public_data.id, public_condition.id))
		self.assertEqual(response_get_public_condition.status_code, 200)

		response_get_public_simulation = c_guest.get('/simulate/stored/%d/' % public_simulation.id)
		self.assertEqual(response_get_public_simulation.status_code, 200)

		response_get_private = c_guest.get('/project/%s/' % str(private_project.folder))
		self.assertEqual(response_get_private.status_code, 403)

		response_get_private_model = c_guest.get('/edit/model/%d/' % private_model.id)
		self.assertEqual(response_get_private_model.status_code, 403)

		response_get_private_data = c_guest.get('/data/%d/' % private_data.id)
		self.assertEqual(response_get_private_data.status_code, 403)

		response_get_private_condition = c_guest.get('/data/%d/%d/' % (private_data.id, private_condition.id))
		self.assertEqual(response_get_private_condition.status_code, 403)

		response_get_private_simulation = c_guest.get('/simulate/stored/%d/' % private_simulation.id)
		self.assertEqual(response_get_private_simulation.status_code, 403)

		response_get_unknown = c_guest.get('/project/slkjvs93rv3f3D/')
		self.assertEqual(response_get_unknown.status_code, 404)

		response_get_unknown_model = c_guest.get('/edit/model/999999999999999999/')
		self.assertEqual(response_get_unknown_model.status_code, 404)

		response_get_unknown_data = c_guest.get('/data/9999999999999999/')
		self.assertEqual(response_get_unknown_data.status_code, 404)

		response_get_unknown_condition = c_guest.get('/data/%d/9983742374/' % public_data.id)
		self.assertEqual(response_get_unknown_condition.status_code, 404)

		response_get_unknown_condition = c_guest.get('/data/999999999999/9983742374/')
		self.assertEqual(response_get_unknown_condition.status_code, 404)

		response_get_unknown_simulation = c_guest.get('/simulate/stored/235252/')
		self.assertEqual(response_get_unknown_simulation.status_code, 404)
