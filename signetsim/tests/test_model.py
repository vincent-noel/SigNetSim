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
from os.path import dirname, join


class TestModels(TestCase):

	fixtures = ["user_with_project.json"]

	def testCreateModel(self):

		user = User.objects.filter(username='test_user')[0]
		self.assertEqual(len(Project.objects.filter(user=user)), 1)
		project = Project.objects.filter(user=user)[0]
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 0)

		c = Client()
		self.assertTrue(c.login(username='test_user', password='password'))

		response_choose_project = c.get('/project/%s/' % project.folder)
		self.assertRedirects(response_choose_project, '/models/', status_code=302, target_status_code=200)


		response_new_model = c.post('/models/', {
			'action': 'new_model',
			'model_name': 'Model 1'
		})

		self.assertEqual(response_new_model.status_code, 200)
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 1)

		created_model = SbmlModel.objects.filter(project=project)[0]
		self.assertEqual(created_model.name, "Model 1")

		files_folder = join(dirname(__file__), "files")
		model_filename = join(files_folder, "modelqlzB7i.xml")

		response_load_model = c.post('/models/', {
			'action': 'load_model',
			'docfile': open(model_filename, 'r')
		})

		self.assertEqual(response_load_model.status_code, 200)
		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 2)

		loaded_model = None
		for t_model in SbmlModel.objects.filter(project=project):
			if t_model != created_model:
				loaded_model = t_model

		self.assertEqual(loaded_model.name, "SOS-Ras-MAPK with n17")

		# Request factory example
		# rf = RequestFactory()
		# post_request = rf.post('/models/', {'action': 'load_model'})
		#
		# middleware = SessionMiddleware()
		# middleware.process_request(post_request)
		# post_request.session.save()
		#
		# post_request.user = user
		# post_request.session['project_id'] = project.id
		# post_request.FILES['file'] = open(model_filename, 'r')
		#
		# response_load_model = ListOfModelsView.as_view()(post_request)
