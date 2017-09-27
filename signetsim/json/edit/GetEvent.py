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

""" GetEvent.py

	This file...

"""

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class GetEvent(JsonRequest, HasWorkingModel):

	def __init__(self):
		JsonRequest.__init__(self)
		HasWorkingModel.__init__(self)

		self.listOfVariables = []

	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)

		event_ind = int(request.POST['event_ind'])

		if event_ind < len(self.getModel().listOfEvents):
			event = self.getModel().listOfEvents.values()[event_ind]

			self.data.update({
				'event_ind': event_ind,
				'event_name': event.getNameOrSbmlId(),
				'event_trigger': event.trigger.getPrettyPrintMathFormula(),
				'event_persistent': 1 if event.trigger.isPersistent else 0,
				'event_initialvalue': 1 if event.trigger.initialValue else 0,
				'event_valuefromtrigger': 1 if event.useValuesFromTriggerTime else 0,
				'event_delay': event.delay.getPrettyPrintMathFormula() if event.delay is not None else "",
				'event_priority': event.priority.getPrettyPrintMathFormula() if event.priority is not None else "",
				'list_of_assignments': [
					(
						self.listOfVariables.index(event_assignment.getVariable()),
						event_assignment.getVariable().getNameOrSbmlId(),
						event_assignment.getDefinition().getPrettyPrintMathFormula()
					)
					for event_assignment in event.listOfEventAssignments
				]
			})

			# for ind, event_assignment in enumerate(event.listOfEventAssignments):
			# 	self.data.update({
			# 		('event_assignment_variable_%d' % ind): self.listOfVariables.index(event_assignment.getVariable()),
			# 		('event_assignment_definition_%d' % ind): event_assignment.getDefinition().getPrettyPrintMathFormula()
			# 	})

		return JsonRequest.post(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)

		for variable in self.getModel().listOfVariables.values():
			if ((variable.isParameter() and variable.isGlobal())
				or variable.isSpecies()
				or variable.isCompartment()
				or variable.isStoichiometry()):

				self.listOfVariables.append(variable)
