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

""" apache.py

	This file...

"""

import os, json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#######################################################################
# HACK ATTACK: this allows Django template tags to span multiple lines.
#######################################################################
import re
from django.template import base

base.tag_re = re.compile(base.tag_re.pattern, re.DOTALL)


# Application definition
INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.templatetags',
	'bootstrap3',
	'signetsim',
	'mod_wsgi.server',
)

from django import __version__
if int(__version__.split('.')[0]) < 2:
	MIDDLEWARE_CLASSES = (
		'django.contrib.sessions.middleware.SessionMiddleware',
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.contrib.auth.middleware.AuthenticationMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
	)


else:
	MIDDLEWARE = (
		'django.contrib.sessions.middleware.SessionMiddleware',
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.contrib.auth.middleware.AuthenticationMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
	)

ROOT_URLCONF = 'signetsim.urls'

TEMPLATES = [
{
	'BACKEND': 'django.template.backends.django.DjangoTemplates',
	'DIRS': [],
	'APP_DIRS': True,
	'OPTIONS': {
		'context_processors': [
			'django.template.context_processors.debug',
			'django.template.context_processors.request',
			'django.contrib.auth.context_processors.auth',
			'django.contrib.messages.context_processors.messages',
		],
	},
},]

WSGI_APPLICATION = 'signetsim.settings.wsgi.application'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'data/db/db.sqlite3'),
	}
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

from random import choice
from string import ascii_uppercase, ascii_lowercase, digits

SECRET_KEY = ''.join(choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(60))

settings_filename = os.path.join(BASE_DIR, "data", "settings", "settings.json")

AUTH_USER_MODEL = 'signetsim.User'

if os.path.isfile(os.path.join(BASE_DIR, "data", "db", "db.sqlite3")):

	if not os.path.isfile(settings_filename):

		RUN_INSTALL = True

		ALLOWED_HOSTS = ["*"]

		STATIC_URL = 'static/'
		STATIC_ROOT = os.path.join(BASE_DIR, "static/")

		MEDIA_URL = 'media/'
		MEDIA_ROOT = os.path.join(BASE_DIR, "data/media/")
	else:

		RUN_INSTALL = False

		with open(settings_filename, 'r') as settings_file:

			settings = json.loads(settings_file.read())

			# signetsim_settings = Settings.objects.all()[0]
			BASE_URL = settings['base_url']

			# SECURITY WARNING: keep the secret key used in production secret!
			SECRET_KEY = settings['secret_key']

			ADMINS = [(settings['admin'], settings['admin_address'])]

			if (
				'email_address' in settings.keys() and
				'email_use_tls' in settings.keys() and
				'email_host' in settings.keys() and
				'email_port' in settings.keys() and
				'email_user' in settings.keys() and
				'email_password' in settings.keys()
			):
				EMAIL_ADDRESS = settings['email_address']
				EMAIL_USE_TLS = settings['email_use_tls']
				EMAIL_HOST = settings['email_host']
				EMAIL_PORT = settings['email_port']
				EMAIL_HOST_USER = settings['email_user']
				EMAIL_HOST_PASSWORD = settings['email_password']

			ALLOWED_HOSTS = settings['allowed_hosts']
			MAX_CORES = settings['max_cores']

		# Static files (CSS, JavaScript, Images)
		# https://docs.djangoproject.com/en/1.10/howto/static-files/

		STATIC_URL = BASE_URL + 'static/'
		STATIC_ROOT = os.path.join(BASE_DIR, "static/")

		MEDIA_URL = BASE_URL + 'media/'
		MEDIA_ROOT = os.path.join(BASE_DIR, "data/media/")

		STATICFILES_DIRS = (
			os.path.join(BASE_DIR, "signetsim/static/"),
		)

else:
	RUN_INSTALL = False

	ALLOWED_HOSTS = ["*"]

	STATIC_URL = '/static/'
	STATIC_ROOT = os.path.join(BASE_DIR, "static/")

	MEDIA_URL = '/media/'
	MEDIA_ROOT = os.path.join(BASE_DIR, "data/media/")

	STATICFILES_DIRS = (
		os.path.join(BASE_DIR, "signetsim/static/"),
	)