#!/usr/bin/env python
""" AnalyseMainView.py


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

from django.views.generic import TemplateView
from django.core.urlresolvers import reverse

from libsignetsim.settings.Settings import Settings

from signetsim.models import SbmlModel
from signetsim.views.HasWorkingModel import HasWorkingModel
from sympy.printing.latex import latex
from sympy.printing.mathml import mathml

from sympy import init_printing
from libsignetsim.model.math.sympy_shortcuts import  (
	SympySymbol, SympyInteger, SympyFloat, SympyRational, SympyAtom,
	SympyOne, SympyNegOne, SympyZero, SympyPi, SympyE, SympyExp1, SympyHalf,
	SympyInf, SympyNan, SympyAdd, SympyMul, SympyPow,
	SympyFunction, SympyUndefinedFunction, SympyLambda, SympyDerivative,
	SympyCeiling, SympyFloor, SympyAbs, SympyLog, SympyExp, SympyPiecewise,
	SympyFactorial, SympyRoot, SympyAcos, SympyAsin, SympyAtan, SympyAcosh,
	SympyAsinh, SympyAtanh, SympyCos, SympySin, SympyTan, SympyAcot,
	SympyAcoth, SympyCosh, SympySinh, SympyTanh, SympySec, SympyCsc,
	SympyCot, SympyCoth, SympyAcsc, SympyAsec,
	SympyEqual, SympyUnequal, SympyGreaterThan, SympyLessThan,
	SympyStrictGreaterThan, SympyStrictLessThan,
	SympyAnd, SympyOr, SympyXor, SympyNot, SympyTrue, SympyFalse,
	SympyMax, SympyMin)
from time import time
from re import match

class AnalyseMainView(TemplateView, HasWorkingModel):

	template_name = 'analyse/main.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)
		# init_printing()
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
		self.loadSystem()

		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		if "action" in request.POST:
			if HasWorkingModel.isChooseModel(self, request):
				self.load(request, *args, **kwargs)

		self.loadSystem()

		self.savePickledModel(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		HasWorkingModel.load(self, request, *args, **kwargs)
		self.modelInstance = self.getModelInstance()

	def loadSystem(self):

		t0 = time()
		# t_instance = self.model.parentDoc.getModelInstance()
		self.modelInstance.build()

		t1 = time()
		print "> build() executed in %.2gs" % (t1-t0)

		function_subs = {}
		symbol_names = {}
		for variable in self.modelInstance.listOfVariables.values():

			is_concentration = False
			t_symbol = variable.symbol.getFinalMathFormula(forcedConcentration=True)
			if isinstance(t_symbol.func, SympyUndefinedFunction):
				t_suffix = "(t)"
				t_name = str(t_symbol.func)
				is_concentration = (t_name.startswith('[') and t_name.endswith(']'))
				if is_concentration:
					t_name = t_name[1:-1]

				function_subs.update({t_symbol: SympySymbol(str(t_symbol.func))})
				t_symbol = SympySymbol(str(t_symbol.func))
			else:
				t_suffix = ""
				t_name = str(t_symbol)

			first = t_name.find('_',1)
			first += 1

			while t_name.find('_', first) > 0:
				first = t_name.find('_', first)
				t_name = t_name[:first] + t_name[first+1:]


			if t_name.find('_') > 0:
				start, end = t_name.split('_')
				t_name = "%s_{%s}" % (start, end)

			if is_concentration:
				t_name = "[%s]" % t_name

			t_name += t_suffix

			symbol_names.update({t_symbol: t_name})


		t2 = time()
		print "> symbols dictionnary built in %.2gs" % (t2-t1)


		self.latex_odes = []
		t_ode_concentrations = self.modelInstance.getODE_concentrations(forcedConcentration=True)
		t20 = time()
		for ode in t_ode_concentrations:
			ode_latex = latex(ode.subs(function_subs), mul_symbol='dot', symbol_names=symbol_names)
			self.latex_odes.append(ode_latex)

		t3 = time()
		print "> got ODEs in %.2gs (%.2gs, %.2gs)" % ((t3-t2), (t20-t2), (t3-t20))


		self.latex_conslaws = []
		if self.modelInstance.hasConservationLaws():
			for conslaw in self.modelInstance.getConservationLaws(forcedConcentration=True):
				cs_latex = latex(conslaw.subs(function_subs), mul_symbol='dot', symbol_names=symbol_names)
				self.latex_conslaws.append(cs_latex)

		t4 = time()
		print "> got conservation laws in %.2gs" % (t4-t3)


		self.latex_cfes = []
		if self.modelInstance.hasCFEs():
			for cfe in self.modelInstance.getCFEs(forcedConcentration=True):
				cfe_latex = latex(cfe.subs(function_subs), mul_symbol='dot', symbol_names=symbol_names)
				self.latex_cfes.append(cfe_latex)

		t5 = time()
		print "> got exact solutions in %.2gs" % (t5-t4)


		self.latex_daes = []
		if self.modelInstance.hasDAEs:
			for dae in self.modelInstance.getDAE_concentrations(forcedConcentration=True):
				dae_latex = latex(dae.subs(function_subs), mul_symbol='dot', symbol_names=symbol_names)
				self.latex_daes.append(dae_latex)

		t6 = time()
		print "> got DAEs in %.2gs" % (t6-t5)
