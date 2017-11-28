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

""" test_archive.py

	This file...

"""

from django.test import TestCase, Client
from django.conf import settings

from signetsim.models import User, Project, SbmlModel, Experiment, SEDMLSimulation
from libsignetsim import CombineArchive

from os.path import dirname, join
from shutil import rmtree


class TestArchive(TestCase):

	fixtures = ["user_with_project.json"]

	def testImportArchive(self):

		user = User.objects.filter(username='test_user')[0]
		self.assertEqual(len(Project.objects.filter(user=user)), 1)
		project = Project.objects.filter(user=user)[0]

		# This test can only run once with success, because the second time the comp model dependencies will
		# actually be in the folder. So cleaning the project folder now
		rmtree(join(join(settings.MEDIA_ROOT, str(project.folder))), "models")

		self.assertEqual(len(SbmlModel.objects.filter(project=project)), 0)

		c = Client()
		self.assertTrue(c.login(username='test_user', password='password'))

		response_choose_project = c.get('/project/%s/' % project.folder)
		self.assertRedirects(response_choose_project, '/models/', status_code=302, target_status_code=200)

		files_folder = join(dirname(__file__), "files")
		archive_filename = join(files_folder, "test_archive.omex")

		response_import_archive = c.post('/', {
			'action': 'load_folder',
			'docfile': open(archive_filename, 'r')
		})

		self.assertEqual(response_import_archive.status_code, 200)
		self.assertEqual(len(Project.objects.filter(user=user)), 2)

		new_project = [t_project for t_project in Project.objects.filter(user=user) if t_project != project][0]

		response_choose_project = c.get('/project/%s/' % new_project.folder)
		self.assertRedirects(response_choose_project, '/models/', status_code=302, target_status_code=200)

		self.assertEqual(len(SbmlModel.objects.filter(project=new_project)), 4)
		self.assertEqual(len(Experiment.objects.filter(project=new_project)), 3)
		self.assertEqual(len(SEDMLSimulation.objects.filter(project=new_project)), 1)

		response_export_archive = c.get('/project_archive/%s/' % new_project.folder)

		self.assertEqual(response_export_archive.status_code, 200)

		path = join(settings.MEDIA_ROOT, 'test_archive_2.omex')
		t_content_file = open(path, "w")
		t_content_file.write(response_export_archive.content)
		t_content_file.close()

		combine_archive = CombineArchive()
		combine_archive.readArchive(path)

		self.assertEqual(len(combine_archive.getAllSbmls()), 4)
		self.assertEqual(len(combine_archive.getAllSedmls()), 1)
		self.assertEqual(len(combine_archive.getAllNumls()), 3)

