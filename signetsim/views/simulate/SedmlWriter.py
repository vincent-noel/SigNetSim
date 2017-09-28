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

""" SedmlWriter.py

	This file ...

"""
from libsignetsim.sedml.SedmlDocument import SedmlDocument

class SedmlWriter(object):


	def __init__(self):
		self.sedml_doc = None

		self.sedml_simulation = None
		self.sedml_model = None
		self.sedml_task = None

	def createUniformTimecourse(self, time_min, time_max, time_ech):

		self.sedml_doc = SedmlDocument()

		self.sedml_simulation = self.sedml_doc.listOfSimulations.createUniformTimeCourse()
		self.sedml_simulation.setInitialTime(time_min)
		self.sedml_simulation.setOutputStartTime(time_min)
		self.sedml_simulation.setOutputEndTime(time_max)
		self.sedml_simulation.setNumberOfPoints(int((time_max - time_min) / time_ech))
		self.sedml_simulation.getAlgorithm().setCVODE()

	def addModel(self, model_filename, modifications=[]):

		self.sedml_model = self.sedml_doc.listOfModels.createModel()
		self.sedml_model.setLanguageSbml()
		self.sedml_model.setSource(model_filename)

		for var, value in modifications:
			change = self.sedml_model.listOfChanges.createChangeAttribute()
			change.setTarget(var)
			change.setNewValue(value)

		self.sedml_task = self.sedml_doc.listOfTasks.createTask()
		self.sedml_task.setModel(self.sedml_model)
		self.sedml_task.setSimulation(self.sedml_simulation)

	def addTimeseries(self, name, variables):

		data_time = self.sedml_doc.listOfDataGenerators.createDataGenerator()
		data_time.setName("Time")
		var_time = data_time.listOfVariables.createVariable()
		var_time.setTask(self.sedml_task)
		var_time.setModel(self.sedml_model)
		var_time.setSymbolTime()
		data_time.getMath().setInternalMathFormula(var_time.getSympySymbol())

		plot2D = self.sedml_doc.listOfOutputs.createPlot2D()

		plot2D.setName(str(name))

		for i_var, variable in enumerate(variables):

			data = self.sedml_doc.listOfDataGenerators.createDataGenerator()
			data.setName(variable.getNameOrSbmlId())
			var = data.listOfVariables.createVariable()
			var.setTask(self.sedml_task)
			var.setModel(self.sedml_model)
			var.setTarget(variable)
			data.getMath().setInternalMathFormula(var.getSympySymbol())

			curve = plot2D.listOfCurves.createCurve()
			curve.setXData(data_time)
			curve.setYData(data)

	def saveSedml(self, filename):
		self.sedml_doc.writeSedmlToFile(filename)

