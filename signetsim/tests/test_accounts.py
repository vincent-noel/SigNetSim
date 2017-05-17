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
		response_signup = c.post('/accounts/register/', {
			'action': 'signup',
			'username': 'test_user',
			'first_name': 'test',
			'last_name': 'user',
			'organization': 'lab',
			'email': 'test_user@mail.com',
			'password1': 'password',
			'password2': 'password'
		})
		print response_signup.content
		self.assertTrue(len(User.objects.filter(is_superuser=False)) == 1)
		new_user = User.objects.filter(is_superuser=False)[0]

		self.assertEqual(new_user.username, 'test_user')
		self.assertEqual(new_user.first_name, "test")
		self.assertEqual(new_user.last_name, "user")
		self.assertEqual(new_user.email, 'test_user@mail.com')
		self.assertEqual(new_user.organization, 'lab')
		self.assertEqual(new_user.is_active, False)
		self.assertRedirects(response_signup, 'accounts/register_success/', status_code=302, target_status_code=200)

		response_login = c.post('/accounts/login/', {
			'action': 'login',
			'username': 'test_user',
			'password': 'password'
		})

		self.assertEqual(response_login.context['getErrors'], ['The user account is not activated yet !'])

		self.assertTrue(c.login(username='admin', password='admin'))

		response_activation = c.get('/accounts/activate_account/', {
			'username': 'test_user'
		})

		self.assertEqual(response_activation.context['activated'], True)

		new_user = User.objects.filter(is_superuser=False)[0]
		self.assertEqual(new_user.is_active, True)

		c.logout()

		response_login_v2 = c.post('/accounts/login/', {
			'action': 'login',
			'username': 'test_user',
			'password': 'password'
		})

		self.assertRedirects(response_login_v2, '/', status_code=302, target_status_code=200)
		self.assertTrue(c.login(username='test_user', password='password'))

		# response_change_fullname = c.post('/profile/test_user/', {
		# 	'action': 'change_fullname',
		# 	'fullname': 'Test User'
		# })
		#
		# self.assertEqual(response_change_fullname.status_code, 200)
		#
		# new_user = User.objects.filter(is_superuser=False)[0]
		# self.assertEqual(new_user.fullname, "Test User")

		response_change_email = c.post('/profile/test_user/', {
			'action': 'change_email',
			'email': 'test_user@signetsim.org'
		})

		self.assertEqual(response_change_email.status_code, 200)

		new_user = User.objects.filter(is_superuser=False)[0]
		self.assertEqual(new_user.email, "test_user@signetsim.org")

		response_change_password = c.post('/profile/test_user/', {
			'action': 'change_password',
			'password1': 'new_password',
			'password2': 'new_password'
		})

		self.assertEqual(response_change_password.status_code, 200)

		c.logout()
		self.assertTrue(c.login(username='test_user', password='new_password'))