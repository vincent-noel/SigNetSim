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

from time import time

class SearchBiomodels(JsonRequest, HasUserLoggedIn):

	def __init__(self):
		JsonRequest.__init__(self)
		HasUserLoggedIn.__init__(self)


	def post(self, request, *args, **kwargs):

		if self.isUserLoggedIn(request):

			search_type = int(request.POST['search_type'])
			search_string = str(request.POST['search_string'])

			try:
				biomodels = BioModels()
				search_res = []

				if search_string != "":
						if search_type == 0:
							search_res = biomodels.getModelsIdByName(search_string)

						elif search_type == 1:
							search_res = biomodels.getModelsIdByPerson(search_string)

						elif search_type == 2:
							search_res = biomodels.getModelsIdByPublication(search_string)

						elif search_type == 3:
							search_res = biomodels.getModelsIdByTaxonomy(search_string)

						elif search_type == 4:
							search_res = biomodels.getModelsIdByUniprot(search_string)

				self.data.update({'results': [model_id for model_id in sorted(search_res) if model_id.startswith("BIOMD")]})

			except:
				self.data.update({'error': "Unable to connect to Biomodels"})

		return JsonRequest.post(self, request, *args, **kwargs)


