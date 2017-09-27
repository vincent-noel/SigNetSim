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

""" AnalyseBifurcationForm.py

	This file ...

"""

from signetsim.views.HasErrorMessages import HasErrorMessages


class AnalyseBifurcationsForm(HasErrorMessages):

	def __init__(self, parent):

		HasErrorMessages.__init__(self)
		self.parent = parent
		self.parameter = None
		self.fromValue = None
		self.toValue = None
		self.variable = None
		self.ds = None
		self.MaxSteps = None

	def read(self, request):

		self.parameter = self.readInt(request, 'parameter_id', "the identifier of the parameter", required=True,
									  max_value=len(self.parent.listOfConstants))

		self.fromValue = self.readFloat(request, 'from_value', "the minimal value to look for equilibrium")
		self.toValue = self.readFloat(request, 'to_value', "the minimal value to look for equilibrium")

		self.variable = self.readInt(request, 'variable_id', "the identifier of the variable", required=True,
									 max_value=len(self.parent.listOfVariables))


		self.ds = self.readFloat(request, 'ds', "the minimal step for parameter modification")
		self.maxSteps = self.readInt(request, 'max_steps', "the maximum number of steps for the algorithm")


