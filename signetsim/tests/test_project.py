#!/usr/bin/env python
""" test_accounts.py


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

from django.test import TestCase, Client
from signetsim.models import User, Project

class TestAccounts(TestCase):

	fixtures = ["test_user.json"]

	def testCreateProject(self):

		user = User.objects.filter(username='test_user')
		self.assertEqual(len(Project.objects.filter(user=user)), 0)

		c = Client()
		self.assertTrue(c.login(username='test_user', password='password'))

		response_create_project = c.post('/', {
			'action': 'new_folder',
			'folder_name': 'Project 1'
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

		



