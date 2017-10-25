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

""" SbmlIdValidator.py

	This file...

"""

from libsbml import SyntaxChecker

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class SbmlIdValidator(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)

	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)
		t_sbml_id = str(request.POST['sbml_id']).strip()

		if (
			'reaction_id' in request.POST
			and request.POST['reaction_id'] != ""
			and int(request.POST['reaction_id']) > 0
		):
			t_reaction = self.getModel().listOfReactions[int(request.POST['reaction_id'])-1]

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

		return JsonRequest.post(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)
