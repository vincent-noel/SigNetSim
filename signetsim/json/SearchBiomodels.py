#!/usr/bin/env python
""" SearchBiomodel.py


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

from signetsim.json import JsonRequest
from signetsim.views.HasUserLoggedIn import HasUserLoggedIn
from bioservices import BioModels


class SearchBiomodels(JsonRequest, HasUserLoggedIn):

	def __init__(self):
		JsonRequest.__init__(self)
		HasUserLoggedIn.__init__(self)


	def post(self, request, *args, **kwargs):

		if self.isUserLoggedIn(request):

			search_type = int(request.POST['search_type'])
			search_string = str(request.POST['search_string'])

			biomodels = BioModels()

			if search_type == 0 and search_string != "":

				results = []

				search_res = biomodels.getModelsIdByName(search_string)
				if search_res is not None and len(search_res) > 0:
					for model_id in sorted(search_res):
						# this will filter out the non-curated ?
						if model_id.startswith("BIOMD"):
							results.append((model_id, biomodels.getModelNameById(model_id)))

				self.data.update({'results': results})

		return JsonRequest.post(self, request, *args, **kwargs)


