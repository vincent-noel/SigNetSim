#!/usr/bin/env python
""" TimeSeriesSimulationView.py


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

from libsignetsim.model.Model import Model
from libsignetsim.model.ModelException import ModelException
from libsignetsim.simulation.TimeseriesSimulation import TimeseriesSimulation
from libsignetsim.simulation.SimulationException import SimulationException
from libsignetsim.data.ExperimentalCondition import ExperimentalCondition
from libsignetsim.data.ExperimentalData import ExperimentalData
from libsignetsim.data.ListOfExperimentalData import ListOfExperimentalData
from libsignetsim.data.Experiment import Experiment as SigNetSimExperiment
from libsignetsim.LibSigNetSimException import UnknownObservationException, UnknownTreatmentException
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.conf import settings
from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.models import SbmlModel, Experiment, Condition, Observation, Treatment, SEDMLSimulation, new_sedml_filename
from signetsim.settings.Settings import Settings
from TimeSeriesSimulationForm import TimeSeriesSimulationForm
from django.shortcuts import redirect

from libsignetsim.sedml.SedmlDocument import SedmlDocument
from os.path import basename, join
from django.core.files import File


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

