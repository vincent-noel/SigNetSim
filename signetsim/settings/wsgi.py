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

""" wsgi.py

	This file...

"""

import os, sys

from django.core.wsgi import get_wsgi_application

root_path = os.path.dirname(os.path.dirname((os.path.abspath(os.path.split(__file__)[0]))))
sys.path.insert(0, root_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "signetsim.settings.apache")

application = get_wsgi_application()
