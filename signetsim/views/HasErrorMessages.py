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

""" HasErrorMessages.py

	This file ...

"""

from libsignetsim import MathFormula
from re import match

class HasErrorMessages(object):

	def __init__(self):
		self.nbErrors = 0
		self.errorMessages = []
		self.errorFields = []

	def get_context_data(self, **kwargs):
		kwargs['hasErrors'] = self.hasErrors()
		kwargs['getErrors'] = self.getErrors()
		kwargs['errorFields'] = self.errorFields
		return kwargs

	def clearErrors(self):
		self.nbErrors = 0
		self.errorMessages = []


	def addError(self, message, reportField=False, field=None):
		self.nbErrors += 1
		self.errorMessages.append(message)
		if reportField and field is not None:
			self.errorFields.append(field)


	def hasErrors(self):
		return self.nbErrors > 0

	def getErrors(self):
		return self.errorMessages

	def printErrors(self):
		for error in self.errorMessages:
			print(error)


	def findMathErrors(self, expression):

		try:
			t_formula = MathFormula(self.parent.model)
			t_formula.setPrettyPrintMathFormula(expression)
			return None

		except Exception as e:
			return e.message


	def existField(self, request, field):

		if request.POST.get(field) is None or str(request.POST[field]) == "":
			return False
		else:
			return True



	def readASCIIString(self, request, field, name, required=True, reportField=True):

		try:
			if request.POST.get(field) is None:
				if required:
					self.addError("%s does not exist !" % name, reportField, field)

			elif request.POST[field] == "":
				if required:
					self.addError("%s is required !" % name, reportField, field)

			else:
				return request.POST[field].encode('utf-8').decode('ascii')

		except UnicodeDecodeError:
			self.addError("Unauthorized special characters in %s" % name)

	def readUnicodeString(self, request, field, name, required=True, reportField=True):

		if request.POST.get(field) is None:
			self.addError("%s does not exist !" % name, reportField, field)

		elif request.POST[field] == "":
			if required:
				self.addError("%s is required !" % name, reportField, field)

		else:
			return request.POST[field]

	def readInt(self, request, field, name, max_value=None, required=True, reportField=True):

		if request.POST.get(field) is None:
			if required:
				self.addError("%s does not exist !" % name, reportField, field)

		elif str(request.POST[field]) == "":
			if required:
				self.addError("%s is required !" % name, reportField, field)

		else:
			try:
				t_int = int(request.POST[field])
				if max_value is not None and t_int >= max_value:
					self.addError("%s is out of bounds !" % name, reportField, field)
				else:
					return t_int

			except ValueError:
				self.addError("%s must be an integer !" % name, reportField, field)

	def readFloat(self, request, field, name, max_value=None, required=True, reportField=True):

		if request.POST.get(field) is None:
			if required:
				self.addError("%s does not exist !" % name, reportField, field)

		elif str(request.POST[field]) == "":
			if required:
				self.addError("%s is required !" % name, reportField, field)
			else:
				return None
		else:
			try:
				t_float = float(request.POST[field])
				if max_value is not None and t_float >= max_value:
					self.addError("%s is out of bounds !" % name, reportField, field)
				else:
					return t_float

			except ValueError:
				if required:
					self.addError("%s must be an float !" % name, reportField, field)




	def readMath(self, request, field, name, required=True, reportField=True):

		if request.POST.get(field) is None:
			self.addError("%s does not exist !" % name,
								reportField, field)

		elif str(request.POST[field]) == "":
			if required:
				self.addError("%s is required !" % name,
								reportField, field)

		else:
			t_errors = self.findMathErrors(str(request.POST[field]))
			if t_errors is None:
				return str(request.POST[field])
			else:
				self.addError("Error in %s : %s" % (name, t_errors),
								reportField, field)


	def readTrueFalse(self, request, field, name, reportField=True):

		if request.POST.get(field) is None:
			self.addError("%s does not exist !" % name,
							reportField, field)

		elif str(request.POST[field]) == "":
			self.addError("%s is required !" % name,
							reportField, field)

		elif str(request.POST[field]) == "0":
			return False

		elif str(request.POST[field]) == "1":
			return True

		else:
			self.addError("%s needs to be either 0 or 1 !" % name,
							reportField, field)


	def readOnOff(self, request, field, name, reportField=True):

		if (request.POST.get(field) is not None
			and str(request.POST[field]) == "on"):

			return True

		else:
			return False


	def readDuration(self, request, field, name, reportField=True):

		t_string = self.readASCIIString(request, field, name, reportField)
		res_match = match(("^"
							+ "(\d{1,2}d){0,1}\s*"
							+ "(\d{1,2}h){0,1}\s*"
							+ "(\d{1,2}m){0,1}\s*"
							+ "(\d{1,2}s){0,1}$")
							, t_string)

		if res_match is None:
			try:
				duration_seconds = float(t_string)
				return duration_seconds

			except:
				self.addError("The format of the %s is incorrect !" % name,
							reportField, field)

		else:
			dur = 0
			if res_match.groups()[0] is not None:
				dur += int(res_match.groups()[0][:-1])*86400
			if res_match.groups()[1] is not None:
				dur += int(res_match.groups()[1][:-1])*3600
			if res_match.groups()[2] is not None:
				dur += int(res_match.groups()[2][:-1])*60
			if res_match.groups()[3] is not None:
				dur += int(res_match.groups()[3][:-1])

			return dur




	def readListInt(self, request, field, name, max_value=None, required=True, reportField=True):

		if request.POST.get(field) is None:
			if required:
				self.addError("%s does not exist !" % name, reportField, field)
			else:
				return []

		elif str(request.POST[field]) == "":
			if required:
				self.addError("%s is required !" % name, reportField, field)
			else:
				return []

		else:
			if request.POST.getlist(field) is not None:
				t_list = request.POST.getlist(field)

				if len(t_list) > 0:

					try:
						f_list = []
						for val in t_list:

							t_int = int(val)
							if max_value is not None and t_int >= max_value:
								self.addError("%s contains elements out of bounds !" % name, reportField, field)
							else:
								f_list.append(t_int)

						return f_list

					except ValueError:
						self.addError("%s's elements must be integers !" % name, reportField, field)

				else:
					self.addError("please select at least one element in %s" % name, reportField, field)
					return []

			elif required:
				self.addError("%s is required !" % name, reportField, field)

			else:
				return []
