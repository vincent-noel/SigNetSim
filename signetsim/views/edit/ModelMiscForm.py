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

""" ModelMiscForm.py

	This file ...

"""

from .ModelParentForm import ModelParentForm

# from django.core.urlresolvers import reverse

# from signetsim.models import SbmlModel
# from signetsim.settings.Settings import Settings

class ModelMiscForm(ModelParentForm):

	def __init__(self, parent):

		ModelParentForm.__init__(self, parent)
		# self.name = None
		# self.notes = None

		self.timeUnit = None
		self.substanceUnit = None
		self.extentUnit = None
		self.scalingFactor = None
		self.sbmlLevel = None


	def clear(self):

		ModelParentForm.clear(self)
		# self.name = None
		# self.notes = None

		self.timeUnit = None
		self.substanceUnit = None
		self.extentUnit = None
		self.scalingFactor = None
		self.sbmlLevel = None


	def load(self):

		# self.name = self.parent.getModel().getName()
		# self.notes = self.parent.getModel().getNotes()

		t_list = self.parent.listOfUnits

		if self.parent.getModel().getTimeUnits() is not None:
			self.timeUnit = t_list.index(self.parent.getModel().getTimeUnits())
		if self.parent.getModel().getSubstanceUnits() is not None:
			self.substanceUnit = t_list.index(self.parent.getModel().getSubstanceUnits())
		if self.parent.getModel().getExtentUnits() is not None:
			self.extentUnit = t_list.index(self.parent.getModel().getExtentUnits())

		if self.parent.getModel().getConversionFactor() is not None:
			self.scalingFactor = self.parent.listOfParameters.index(self.parent.getModel().getConversionFactor())

		self.sbmlLevel = self.parent.getModel().getSbmlLevels().index(self.parent.getModel().sbmlLevel)



	###########################################################################
	# Time unit
	def readTimeUnit(self, request):

		self.timeUnit = self.readInt(request,
							'time_unit_id', "The time unit of the model",
							max_value=len(self.parent.listOfUnits))

	def saveTimeUnit(self):

		if self.timeUnit is not None:
			self.parent.getModel().setTimeUnits(
				self.parent.listOfUnits[self.timeUnit].getSbmlId()
			)
		else:
			self.parent.getModel().setTimeUnits(None)

	def clearTimeUnits(self):
		self.timeUnit = None



	###########################################################################
	# Substance unit
	def readSubstanceUnit(self, request):

		self.substanceUnit = self.readInt(request,
							'substance_unit_id', "The substance unit of the model",
							max_value=len(self.parent.listOfUnits))

	def saveSubstanceUnit(self):

		if self.substanceUnit is not None:
			self.parent.getModel().setSubstanceUnits(
				self.parent.listOfUnits[self.substanceUnit].getSbmlId()
			)
		else:
			self.parent.getModel().setSubstanceUnits(None)


	def clearSubstanceUnits(self):
		self.substanceUnit = None


	###########################################################################
	# Extent unit
	def readExtentUnit(self, request):

		self.extentUnit = self.readInt(request,
							'extent_unit_id', "The extent unit of the model",
							max_value=len(self.parent.listOfUnits))

	def saveExtentUnit(self):

		if self.extentUnit is not None:
			self.parent.getModel().setExtentUnits(
				self.parent.listOfUnits[self.extentUnit].getSbmlId()
			)
		else:
			self.parent.getModel().setExtentUnits(None)

	def clearExtentUnit(self):
		self.extentUnit = None


	###########################################################################
	# Scaling factor
	def readScalingFactor(self, request):

		self.scalingFactor = self.readInt(request,
							'scaling_factor_id', "The scaling of the model",
							max_value=len(self.parent.listOfUnits))

	def saveScalingFactor(self):

		if self.scalingFactor is not None:
			self.parent.getModel().setConversionFactor(
				self.parent.listOfParameters[self.scalingFactor].getSbmlId()
			)
		else:
			self.parent.getModel().setConversionFactor(None)

	def clearScalingFactor(self):
		self.scalingFactor = None


	# ###########################################################################
	# # Name
	# def readName(self, request):
	#
	# 	self.name = self.readString(request,
	# 						'model_name', "The name of the model")
	#
	# def saveName(self):
	# 	self.parent.getModel().setName(self.name)


	# ###########################################################################
	# # Notes
	# def readNotes(self, request):
	#
	# 	self.notes = self.readString(request,
	# 						'model_notes', "The notes of the model")
	# def saveNotes(self):
	# 	self.parent.getModel().setNotes(self.notes)


	###########################################################################
	# Sbml Level
	def readSbmlLevel(self, request):

		self.sbmlLevel = self.readInt(request,
							'model_sbml_level', "The SBML level of the model",
							max_value=len(self.parent.sbmlLevels))
	def saveSbmlLevel(self):
		self.parent.getModel().setSbmlLevel(self.parent.sbmlLevels[self.sbmlLevel])
