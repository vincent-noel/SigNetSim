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

""" AnalyseBifurcationView.py

	This file ...

"""

from libsignetsim.continuation.EquilibriumPointCurve import EquilibriumPointCurve
from django.views.generic import TemplateView
from signetsim.views.HasErrorMessages import HasErrorMessages
from signetsim.models import Continuation, SbmlModel
from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.views.analyse.AnalyseBifurcationForm import AnalyseBifurcationsForm
from signetsim.settings.Settings import Settings
from signetsim.managers.computations import add_computation
import dill


class AnalyseBifurcationsView(TemplateView, HasWorkingModel, HasErrorMessages):

	template_name = 'analyse/bifurcations.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)
		HasErrorMessages.__init__(self)

		self.listOfConstants = None
		self.listComputations = None
		self.computation = None

		self.form = AnalyseBifurcationsForm(self)

	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)
		kwargs['list_of_constants'] = [const.getNameOrSbmlId() for const in self.listOfConstants]
		kwargs['list_of_computations'] = self.listOfComputations
		kwargs['colors'] = Settings.default_colors
		kwargs['form'] = self.form

		return kwargs

	def get(self, request, *args, **kwargs):
		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingModel.isChooseModel(self, request):
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "compute_curve":
				self.computeCurve(request)
				self.loadComputations()

			elif request.POST['action'] == "delete":
				self.deleteCurve(request)
				self.loadComputations()

		return TemplateView.get(self, request, *args, **kwargs)

	def deleteCurve(self, request):
		curve_id = self.readInt(request, 'result_id', "The id of the curve to delete")
		t_computation = Continuation.objects.get(id=curve_id)
		t_computation.delete()

	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)
		HasErrorMessages.clearErrors(self)
		self.loadConstants()
		self.loadComputations()

	def loadConstants(self):
		self.getModelInstance().listOfVariables.classifyVariables()
		self.listOfConstants = [variable for variable in self.getModelInstance().listOfVariables if variable.isConstant()]

	def loadComputations(self):
		t_model = SbmlModel.objects.get(project=self.project_id, id=self.model_id)
		self.listOfComputations = Continuation.objects.filter(project=self.project, model=t_model)

	def computeCurve(self, request):
		if self.isProjectOwner(request):
			self.form.read(request)
			if not self.form.hasErrors():

				t_model = SbmlModel.objects.get(project=self.project_id, id=self.model_id)

				self.computation = Continuation(
					project=self.project,
					model=t_model,
					parameter=self.listOfConstants[self.form.parameter].getSymbolStr(),
				)

				self.computation.save()

				t_ep_curve = EquilibriumPointCurve(self.getModelInstance())
				t_ep_curve.setParameter(self.listOfConstants[self.form.parameter])
				t_ep_curve.setRange(self.form.fromValue, self.form.toValue)
				t_ep_curve.setDs(self.form.ds)
				t_ep_curve.setMaxSteps(self.form.maxSteps)
				t_ep_curve.build()

				add_computation(
					project=self.project,
					entry=self.computation,
					object=t_ep_curve
				)
		else:

			self.form.addError(
				"You are not the owner of this project. Please make a local copy if you want to compute equilibrium curve.")

