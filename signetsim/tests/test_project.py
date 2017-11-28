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

""" test_project.py

	This file tests the creation, copy, deletion, modification and sharing of projects

"""

from django.test import TestCase, Client
from django.conf import settings

from signetsim.models import User, Project

from json import loads


class TestProjects(TestCase):

	fixtures = ["users.json"]

	def testCreateProject(self):

		user = User.objects.filter(username='test_user')
		self.assertEqual(len(Project.objects.filter(user=user)), 0)

		c = Client()
		self.assertTrue(c.login(username='test_user', password='password'))

		response_create_project = c.post('/', {
			'action': 'new_folder',
			'project_name': 'Project 1'
		})

		self.assertEqual(response_create_project.status_code, 200)
		self.assertEqual(len(Project.objects.filter(user=user)), 1)

		project = Project.objects.filter(user=user)[0]

		self.assertEqual(project.name, "Project 1")

		response_copy_project = c.post('/', {
			'action': 'copy_folder',
			'id': project.id
		})

		self.assertEqual(response_copy_project.status_code, 200)
		self.assertEqual(len(Project.objects.filter(user=user)), 2)

		other_project = None
		for t_project in Project.objects.filter(user=user):
			if t_project != project:
				other_project = t_project

		self.assertEqual(other_project.name, u"Project 1 (Copy)")

		response_delete_project = c.post('/', {
			'action': 'delete_folder',
			'id': other_project.id
		})

		self.assertEqual(response_delete_project.status_code, 200)
		self.assertEqual(len(Project.objects.filter(user=user)), 1)
		self.assertEqual(Project.objects.filter(user=user)[0], project)

		user_2 = User.objects.filter(username='test_user_2')
		self.assertEqual(len(Project.objects.filter(user=user_2)), 0)

		response_send_project = c.post('/', {
			'action': 'send_folder',
			'id': project.id,
			'username': 'test_user_2'
		})

		self.assertEqual(response_send_project.status_code, 200)
		self.assertEqual(len(Project.objects.filter(user=user)), 1)
		self.assertEqual(len(Project.objects.filter(user=user_2)), 1)

		response_get_project = c.post('/json/get_project/', {
			'id': project.id
		})

		self.assertEqual(response_get_project.status_code, 200)
		json_response = loads(response_get_project.content)

		self.assertEqual(json_response['name'], u'Project 1')
		self.assertEqual(json_response['public'], 0)

		response_set_project_public = c.post('/', {

			'action': 'save_project',
			'project_id': project.id,
			'project_name': "Public project",
			'project_access': 'on',
		})

		self.assertEqual(response_set_project_public.status_code, 200)

		response_get_project = c.post('/json/get_project/', {
			'id': project.id
		})

		self.assertEqual(response_get_project.status_code, 200)
		json_response = loads(response_get_project.content)

		self.assertEqual(json_response['name'], u'Public project')
		self.assertEqual(json_response['public'], 1)

		response_set_project_private = c.post('/', {

			'action': 'save_project',
			'project_id': project.id,
			'project_name': "Private project",
		})

		self.assertEqual(response_set_project_private.status_code, 200)
		response_get_project = c.post('/json/get_project/', {
			'id': project.id
		})

		self.assertEqual(response_get_project.status_code, 200)
		json_response = loads(response_get_project.content)

		self.assertEqual(json_response['name'], u'Private project')
		self.assertEqual(json_response['public'], 0)