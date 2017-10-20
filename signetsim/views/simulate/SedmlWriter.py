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

	def createDocument(self):
		self.sedml_doc = SedmlDocument()

	def createUniformTimecourse(self, time_min, time_max, time_ech):

		sedml_simulation = self.sedml_doc.listOfSimulations.createUniformTimeCourse()
		sedml_simulation.setInitialTime(time_min)
		sedml_simulation.setOutputStartTime(time_min)
		sedml_simulation.setOutputEndTime(time_max)
		sedml_simulation.setNumberOfPoints(int((time_max - time_min) / time_ech))
		sedml_simulation.getAlgorithm().setCVODE()

		return sedml_simulation

	def createSteadyStates(self):

		sedml_simulation = self.sedml_doc.listOfSimulations.createSteadyState()
		sedml_simulation.getAlgorithm().setKinSol()

		return sedml_simulation

	def addModel(self, model_filename, modifications=[], var_input=None):

		sedml_model = self.sedml_doc.listOfModels.createModel()
		sedml_model.setLanguageSbml()
		sedml_model.setSource(model_filename)

		if var_input is not None:
			addXMLParameter = sedml_model.listOfChanges.createAddXML()
			addXMLParameter.getTarget().readSedml("/sbml:sbml/sbml:model/sbml:listOfParameters")
			addXMLParameter.setNewXMLFromString("<parameter id=\"steady_states__input_value\"/>")

			addXMLInitialAssignment = sedml_model.listOfChanges.createAddXML()
			addXMLInitialAssignment.getTarget().readSedml("/sbml:sbml/sbml:model/sbml:listOfInitialAssignments")
			addXMLInitialAssignment.setNewXMLFromString(
				"<initialAssignment symbol=\"%s\">" % var_input.getSbmlId()
				+ "<math xmlns=\"http://www.w3.org/1998/Math/MathML\"><ci>steady_states__input_value</ci></math>"
				+ "</initialAssignment>"
			)

		for var, value in modifications:
			change = sedml_model.listOfChanges.createChangeAttribute()
			change.setTarget(var)
			change.setNewValue(value)

		return sedml_model

	def addTimeseriesCurve(self, timecourse, model, name, variables):

		sedml_task = self.sedml_doc.listOfTasks.createTask()
		sedml_task.setModel(model)
		sedml_task.setSimulation(timecourse)

		data_time = self.sedml_doc.listOfDataGenerators.createDataGenerator()
		data_time.setName("Time")
		var_time = data_time.listOfVariables.createVariable()
		var_time.setTask(sedml_task)
		var_time.setModel(model)
		var_time.setSymbolTime()
		data_time.getMath().setInternalMathFormula(var_time.getSympySymbol())

		plot2D = self.sedml_doc.listOfOutputs.createPlot2D()

		plot2D.setName(str(name))

		for i_var, variable in enumerate(variables):

			data = self.sedml_doc.listOfDataGenerators.createDataGenerator()
			data.setName(variable.getNameOrSbmlId())
			var = data.listOfVariables.createVariable()
			var.setTask(sedml_task)
			var.setModel(model)
			var.setTarget(variable)
			data.getMath().setInternalMathFormula(var.getSympySymbol())

			curve = plot2D.listOfCurves.createCurve()
			curve.setXData(data_time)
			curve.setYData(data)


	def addSteadyStatesCurve(self, steady_states, model, name, variables, values, variable_input):

		task = self.sedml_doc.listOfTasks.createTask()
		task.setModel(model)
		task.setSimulation(steady_states)

		repeated_task = self.sedml_doc.listOfTasks.createRepeatedTask()
		repeated_task.setResetModel(True)

		vector_range = repeated_task.listOfRanges.createVectorRange()
		vector_range.setValues(values)
		repeated_task.setRange(vector_range)

		set_value = repeated_task.listOfSetValueChanges.createSetValue()
		set_value.setModel(model)
		set_value.getTarget().readSedml("/sbml:sbml/sbml:model/sbml:listOfParameters/parameter[@id='steady_states__input_value']")
		set_value.setRange(vector_range)
		set_value.getMath().setInternalMathFormula(vector_range.getSymbol())

		sub_task = repeated_task.listOfSubTasks.createSubTask()
		sub_task.setTask(task)
		sub_task.setOrder(1)

		data_input = self.sedml_doc.listOfDataGenerators.createDataGenerator()
		data_input.setName(variable_input.getNameOrSbmlId())
		var_input = data_input.listOfVariables.createVariable()
		var_input.setTask(repeated_task)
		var_input.setModel(model)
		var_input.getTarget().readSedml("/sbml:sbml/sbml:model/sbml:listOfParameters/parameter[@id='steady_states__input_value']")
		data_input.getMath().setInternalMathFormula(var_input.getSympySymbol())

		plot2D = self.sedml_doc.listOfOutputs.createPlot2D()

		plot2D.setName(str(name))

		for i_var, variable in enumerate(variables):

			data = self.sedml_doc.listOfDataGenerators.createDataGenerator()
			data.setName(variable.getNameOrSbmlId())
			var = data.listOfVariables.createVariable()
			var.setTask(repeated_task)
			var.setModel(model)
			var.setTarget(variable)
			data.getMath().setInternalMathFormula(var.getSympySymbol())

			curve = plot2D.listOfCurves.createCurve()
			curve.setXData(data_input)
			curve.setYData(data)

	def saveSedml(self, filename):
		self.sedml_doc.writeSedmlToFile(filename)

