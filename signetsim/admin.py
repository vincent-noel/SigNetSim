#!/usr/bin/env python
""" admin.py


	This file ...


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

from django.contrib import admin

# Register your models here.
from .models import User, Project, SbmlModel#, FittedSbmlModel
# from .models import Project, SbmlModel, FittedSbmlModel
# from django.contrib.auth.models import User
from .models import Optimization, ContinuationComputation
from .models import Experiment, Condition, Observation, Treatment

admin.site.register(User)
admin.site.register(Project)
admin.site.register(SbmlModel)

# admin.site.register(FittedSbmlModel)
admin.site.register(Optimization)
admin.site.register(ContinuationComputation)


admin.site.register(Experiment)
admin.site.register(Condition)
admin.site.register(Observation)
admin.site.register(Treatment)
