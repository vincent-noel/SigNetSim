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
from signetsim.models import User

class TestAccounts(TestCase):

	fixtures = ["basic.json"]

	def testCreateUser(self):

		self.assertTrue(len(User.objects.filter(is_superuser=False)) == 0)

		c = Client()
		response = c.post('/accounts/register/', {
			'action': 'signup',
			'username': 'labestiol',
			'fullname': '',
			'email': 'labestiol@gmail.com',
			'password1': 'password',
			'password2': 'password'
		})

		self.assertTrue(len(User.objects.filter(is_superuser=False)) == 1)
		new_user = User.objects.filter(is_superuser=False)[0]

		self.assertEqual(new_user.username, 'labestiol')
		self.assertEqual(new_user.fullname, None)
		self.assertEqual(new_user.email, 'labestiol@gmail.com')
		self.assertRedirects(response, 'accounts/register_success/', status_code=302, target_status_code=200)





