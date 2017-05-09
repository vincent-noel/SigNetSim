#!/usr/bin/env python
""" SbmlIdValidator.py


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
from libsignetsim.model.math.MathFormula import MathFormula
from libsignetsim.model.ModelException import ModelException
from libsbml import SyntaxChecker

class SbmlIdValidator(JsonView, HasWorkingModel):

	def __init__(self):
		JsonView.__init__(self)
		HasWorkingModel.__init__(self)

	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)
		t_sbml_id = str(request.POST['sbml_id']).strip()

		t_reaction_id = None
		if ('reaction_id' in request.POST
			and
			request.POST['reaction_id'] != ""
		):
			t_reaction = self.getModel().listOfReactions[int(request.POST['reaction_id'])]
			# print t_reaction.listOfLocalParameters.sbmlIds()
			if t_reaction.listOfLocalParameters.containsSbmlId(t_sbml_id):

				self.data.update({'error': 'sbml id already exists in reaction %s' % t_reaction.getName()})
			elif not SyntaxChecker.isValidSBMLSId(str(request.POST['sbml_id'])):
				self.data.update({'error': 'sbml id is not valid'})

			else:
				self.data.update({'error': ''})


		elif self.getModel().listOfVariables.containsSbmlId(t_sbml_id):
			self.data.update({'error': 'sbml id already exists'})

		elif not SyntaxChecker.isValidSBMLSId(str(request.POST['sbml_id'])):
			self.data.update({'error': 'sbml id is not valid'})

		else:
			self.data.update({'error': ''})

		return JsonView.post(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)
