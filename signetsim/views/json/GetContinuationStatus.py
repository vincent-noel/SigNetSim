#!/usr/bin/env python
""" GetContinuationStatus.py


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

from signetsim.views.json.JsonView import JsonView
from signetsim.views.HasWorkingModel import HasWorkingModel

from signetsim.models import SbmlModel, ContinuationComputation

class GetContinuationStatus(JsonView, HasWorkingModel):

	def __init__(self):
		JsonView.__init__(self)
		HasWorkingModel.__init__(self)
		self.listOfComputations = None


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		t_str = request.POST['continuation_id']

		if t_str != "":
			t_id = int(t_str)
			t_computation = self.listOfComputations[t_id]
			self.data.update({'status': str(t_computation.status)})

		return JsonView.post(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)
		t_model = SbmlModel.objects.get(project=self.project_id, id=self.model_id)
		self.listOfComputations = ContinuationComputation.objects.filter(project=self.project, model=t_model)
