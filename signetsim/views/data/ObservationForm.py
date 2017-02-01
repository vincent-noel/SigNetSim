#!/usr/bin/env python
""" ObservationForm.py


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

from signetsim.views.ParentForm import ParentForm
from signetsim.models import Observation

class ObservationForm(ParentForm):

	def __init__(self, parent):

		ParentForm.__init__(self, parent)

		self.id = None
		self.name = None
		self.time = None
		self.value = None
		self.stddev = None
		self.steadyState = False
		self.minTimeSteadyState = None
		self.maxTimeSteadyState = None

	def clear(self):

		ParentForm.clear(self)
		self.id = None
		self.name = None
		self.time = None
		self.value = None
		self.stddev = None
		self.steadyState = False
		self.minTimeSteadyState = None
		self.maxTimeSteadyState = None


	def load(self, request):

		t_observation_id = self.readInt(request, 'id',
									"The identifier of the observation to load")

		if t_observation_id is not None:
			observation = Observation.objects.get(id=t_observation_id)
			self.id = observation.id
			self.name = observation.species
			self.time = observation.time
			self.value = observation.value
			self.stddev = observation.stddev
			self.steadyState = observation.steady_state
			self.minTimeSteadyState = observation.min_steady_state
			self.maxTimeSteadyState = observation.max_steady_state
			self.isEditing = True


	def save(self):

		if self.isNew():
			observation = Observation(condition=self.parent.condition)

		else:
			observation = Observation.objects.get(id=self.id)

		observation.species = self.name
		observation.time = self.time
		observation.value = self.value
		observation.stddev = self.stddev
		observation.steady_state = self.steadyState
		observation.min_steady_state = self.minTimeSteadyState
		observation.max_steady_state = self.maxTimeSteadyState
		observation.save()

	def read(self, request):

		self.id = self.readInt(request, 'id',
								"The identifier of the observation", required=False)

		self.name = self.readString(request, 'name',
									"The name of the observed species")

		self.time = self.readFloat(request, 'time',
									"The time of the observation")

		self.value = self.readFloat(request, 'value',
									"The value of the observation")

		self.stddev = self.readFloat(request, 'stddev',
									"The standard deviation of the observation")

		self.steadyState = self.readOnOff(request, 'steady_state',
				"The settings describing if the observation is at steady state")

		print self.steadyState
		self.minTimeSteadyState = self.readFloat(request, 'min_steady_state',
									"The minimum time to reach steady state",
													required=self.steadyState)

		self.maxTimeSteadyState = self.readFloat(request, 'max_steady_state',
									"The maximum time to reach steady state",
													required=self.steadyState)
