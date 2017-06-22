#!/usr/bin/env python
""" TreatmentForm.py


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
from signetsim.models import Treatment

class TreatmentForm(ParentForm):

	def __init__(self, parent):

		ParentForm.__init__(self, parent)

		self.id = None
		self.name = None
		self.time = None
		self.value = None


	def clear(self):

		ParentForm.clear(self)
		self.id = None
		self.name = None
		self.time = None
		self.value = None


	def load(self, request):

		t_treatment_id = self.readInt(request, 'id',
									"The identifier of the treatment")
		# print request.POST['id']
		# print t_treatment_id

		self.printErrors()
		if t_treatment_id is not None:
			treatment = Treatment.objects.get(id=t_treatment_id)
			self.id = treatment.id
			self.name = treatment.species
			self.time = treatment.time
			self.value = treatment.value
			self.isEditing = True
			# print self.isEditing


	def save(self):

		if self.isNew():
			treatment = Treatment(condition=self.parent.condition)
		else:
			treatment = Treatment.objects.get(id=self.id)

		treatment.species = self.name
		treatment.time = self.time
		treatment.value = self.value

		treatment.save()

	def read(self, request):

		self.id = self.readInt(request, 'id',
								"The identifier of the treatment", required=False)

		self.name = self.readString(request, 'name',
									"The name of the treated species")

		self.time = self.readFloat(request, 'time',
									"The time of the treatment")

		self.value = self.readFloat(request, 'value',
									"The value of the treatment")
