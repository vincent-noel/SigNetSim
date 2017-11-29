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

""" ModelEventsForm.py

	This file ...

"""

from ModelParentForm import ModelParentForm

class ModelEventsForm(ModelParentForm):

	def __init__(self, parent):

		ModelParentForm.__init__(self, parent)

		self.name = None
		self.sbmlId = None
		self.trigger = ""
		self.delay = None
		self.priority = None
		self.initialvalue = False
		self.persistent = True
		self.assignments = [(None, None)]
		self.useValuesFromTriggerTime = False


	def save(self, event):

		event.setName(self.name)
		event.setSbmlId(self.sbmlId)
		event.setTrigger(self.trigger)
		event.setDelay(self.delay)
		event.setPriority(self.priority)

		event.setTriggerInitialValue(self.initialvalue)
		event.setTriggerPersistent(self.persistent)
		event.setUseValuesFromTriggerTime(self.useValuesFromTriggerTime)

		event.listOfEventAssignments = []
		for assignment in self.assignments:
			t_assignment = event.addEventAssignment()
			t_variable = self.parent.listOfVariables[assignment[0]]
			t_assignment.setVariable(t_variable)
			t_assignment.getDefinition().setPrettyPrintMathFormula(assignment[1])



	def read(self, request):

		self.id = self.readInt(request, 'event_id',
								"The indice of the event", required=False)

		self.name = self.readString(request, 'event_name',
									"The name of the event", required=False)
		self.sbmlId = self.readString(request, 'event_sbmlid',
									"The identifier of the event")

		self.readTrigger(request)
		self.readAssignments(request)
		self.readOptions(request)

		self.printErrors()
	def readTrigger(self, request):

		self.trigger = self.readMath(request, 'event_trigger',
										"The trigger of the event")

	def readAssignments(self, request):

		nb_assignment = 0

		while ("event_assignment_%d_id" % nb_assignment) in request.POST:
			if nb_assignment == 0:
				self.assignments = []

			t_assignment = self.readInt(request,
									('event_assignment_%d_id' % nb_assignment),
						"The variable for the assignment #%d" % nb_assignment,
						max_value=len(self.parent.listOfVariables))

			t_assignment_expression = self.readMath(request,
							('event_assignment_%d_expression' % nb_assignment),
					"The assignment for the assignment #%d" % nb_assignment)

			if t_assignment is not None:
				self.assignments.append((t_assignment, t_assignment_expression))

			nb_assignment += 1

		if nb_assignment < 1:
			self.addError("Event need at least one assignment")


	def readOptions(self, request):


		self.priority = self.readMath(request, 'event_priority',
								"The priority of the event", required=False)


		self.delay = self.readMath(request, 'event_delay',
									"The delay of the event", required=False)


		self.persistent = self.readOnOff(request, 'event_persistent',
										"The persistent property of the event")

		self.initialvalue = self.readOnOff(request, 'event_initialvalue',
											"The initial value of the event")

		self.useValuesFromTriggerTime = self.readOnOff(request,
														'event_usetriggertime',
					"The use values from trigger time property of the event")
