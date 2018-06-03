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

""" AdminView.py

	This file ...

"""

from django.views.generic import TemplateView
from signetsim.models import ComputationQueue, Continuation, Optimization
from signetsim.views.HasErrorMessages import HasErrorMessages
from signetsim.managers.computations import update_queue


class ComputationsView(TemplateView, HasErrorMessages):
	template_name = 'admin/computations.html'


	def __init__(self, **kwargs):
		TemplateView.__init__(self, **kwargs)
		HasErrorMessages.__init__(self)

		self.computations = None
		self.computationsStatus = None
		self.conts = None
		self.optims = None

	def get_context_data(self, **kwargs):
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)
		kwargs['computations'] = self.computations
		kwargs['comp_statuses'] = self.computationsStatus
		kwargs['conts'] = self.conts
		kwargs['optims'] = self.optims
		return kwargs

	def get(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)
		if "action" in request.POST:
			if request.POST['action'] == "delete":
				self.deleteComputation(request)

			elif request.POST['action'] == "delete_cont":
				self.deleteContinuation(request)

			elif request.POST['action'] == "delete_optim":
				self.deleteOptimization(request)

			elif request.POST['action'] == "update_queue":
				self.updateQueue(request)

		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):
		self.loadContinuations()
		self.loadOptimizations()
		self.loadComputations()

	def loadContinuations(self):
		self.conts = [cont for cont in Continuation.objects.all() if cont.status == Continuation.BUSY]

	def loadOptimizations(self):
		self.optims = [optim for optim in Optimization.objects.all() if optim.status == Optimization.BUSY]

	def loadComputations(self):
		self.computations = ComputationQueue.objects.all()
		self.computationsStatus = ["Optimization" if comp.type == ComputationQueue.OPTIM else "Continuation" for comp in
								   self.computations]

	def deleteComputation(self, request):

		if ComputationQueue.objects.filter(id=int(request.POST['id'])).exists():

			comp = ComputationQueue.objects.get(id=int(request.POST['id']))
			comp.delete()
			self.loadComputations()


	def deleteContinuation(self, request):

		if Continuation.objects.filter(id=int(request.POST['id'])).exists():

			cont = Continuation.objects.get(id=int(request.POST['id']))
			cont.delete()
			self.loadContinuations()


	def deleteOptimization(self, request):

		if Optimization.objects.filter(id=int(request.POST['id'])).exists():

			optim = Optimization.objects.get(id=int(request.POST['id']))
			optim.delete()
			self.loadOptimizations()

	def updateQueue(self, request):

		update_queue()