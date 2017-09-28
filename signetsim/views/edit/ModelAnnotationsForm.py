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

""" ModelAnnotationsForm.py

	This file ...

"""

from ModelParentForm import ModelParentForm

class ModelAnnotationsForm(ModelParentForm):

	def __init__(self, parent):

		ModelParentForm.__init__(self, parent)
		self.name = None
		self.notes = None

	def clear(self):

		ModelParentForm.clear(self)
		self.name = None
		self.notes = None

	def load(self):

		self.name = self.parent.getModel().getName()
		self.notes = self.parent.getModel().getNotes()

	def readName(self, request):

		self.name = self.readString(request,
							'model_name', "The name of the model")

	def saveName(self):
		self.parent.getModel().setName(self.name)

	def readNotes(self, request):

		self.notes = self.readString(request,
							'model_notes', "The notes of the model")
	def saveNotes(self):
		self.parent.getModel().setNotes(self.notes)

