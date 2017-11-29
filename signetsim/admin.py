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

""" admin.py

	This file ...

"""

from django.contrib import admin

# Register your models here.
from .models import User, Project, SbmlModel, SEDMLSimulation, CombineArchiveModel
from .models import Optimization, ContinuationComputation
from .models import Experiment, Condition, Observation, Treatment
from .models import Settings

admin.site.register(User)
admin.site.register(Project)
admin.site.register(SbmlModel)
admin.site.register(SEDMLSimulation)
admin.site.register(CombineArchiveModel)
admin.site.register(Optimization)
admin.site.register(ContinuationComputation)


admin.site.register(Experiment)
admin.site.register(Condition)
admin.site.register(Observation)
admin.site.register(Treatment)

admin.site.register(Settings)
