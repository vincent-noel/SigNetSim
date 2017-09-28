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

""" AnalyseMainView.py

	This file ...

"""

from django.views.generic import TemplateView

from signetsim.views.HasWorkingModel import HasWorkingModel

from libsignetsim.model.math.MathDevelopper import unevaluatedSubs

from sympy import expand
from sympy.printing.latex import latex


class AnalyseMainView(TemplateView, HasWorkingModel):

	template_name = 'analyse/main.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)

		self.modelInstance = None
		self.latex_odes = []
		self.latex_conslaws = []
		self.latex_cfes = []
		self.latex_daes = []


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs['latex_odes'] = self.latex_odes
		kwargs['latex_conslaws'] = self.latex_conslaws
		kwargs['latex_cfes'] = self.latex_cfes
		kwargs['latex_daes'] = self.latex_daes
		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		if "action" in request.POST:
			if HasWorkingModel.isChooseModel(self, request):
				self.load(request, *args, **kwargs)

			elif request.POST['action'] == "show_reduced":
				self.loadReducedSystem()
				self.loadSystemComponents()

		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)
		self.modelInstance = self.getModelInstance()
		self.loadSystem()
		self.loadSystemComponents()

	def loadSystem(self):
		self.modelInstance.build()

	def loadReducedSystem(self):
		self.modelInstance.buildReducedModel()

	def loadSystemComponents(self):

		function_subs = {}
		symbol_names = {}

		self.latex_odes = []
		for ode in self.modelInstance.getMathModel().listOfODEs:

			ode_formula = ode.getFormula(developped=True)
			ode_latex = latex(unevaluatedSubs(expand(ode_formula), function_subs), mul_symbol='dot', symbol_names=symbol_names)
			self.latex_odes.append(ode_latex)

		self.latex_conslaws = []
		for conslaw in self.modelInstance.listOfConservationLaws:
			conslaw_formula = conslaw.getFormula()
			cs_latex = latex(unevaluatedSubs(expand(conslaw_formula), function_subs), mul_symbol='dot', symbol_names=symbol_names)
			self.latex_conslaws.append(cs_latex)

		self.latex_cfes = []
		for cfe in self.modelInstance.getMathModel().listOfCFEs:
			cfe_formula = cfe.getFormula(developped=True)
			cfe_latex = latex(unevaluatedSubs(expand(cfe_formula), function_subs), mul_symbol='dot', symbol_names=symbol_names)
			self.latex_cfes.append(cfe_latex)

		self.latex_daes = []
		for dae in self.modelInstance.getMathModel().listOfDAEs:
			dae_formula = dae.getFormula(developped=True)
			dae_latex = latex(unevaluatedSubs(expand(dae_formula), function_subs), mul_symbol='dot', symbol_names=symbol_names)
			self.latex_daes.append(dae_latex)
