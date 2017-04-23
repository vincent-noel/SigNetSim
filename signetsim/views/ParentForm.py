#!/usr/bin/env python
""" ParentForm.py


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

from libsignetsim.model.math.MathFormula import MathFormula
# from libsignetsim.model.ModelException import ModelException
from signetsim.views.HasErrorMessages import HasErrorMessages


class ParentForm(HasErrorMessages):

	def __init__(self, parent):

		HasErrorMessages.__init__(self)
		self.parent = parent
		self.id = None
		self.isEditing = False
		self.clear()


	def isNew(self):
		return self.id is None

	def clear(self):
		self.clearErrors()


	def findMathErrors(self, expression):

		try:
			t_formula = MathFormula(self.parent.model)
			t_formula.setPrettyPrintMathFormula(expression)
			return None

		except Exception as e:
			return e.message
