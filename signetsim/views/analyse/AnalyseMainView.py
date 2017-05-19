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

from sympy import init_printing, expand, simplify
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
from libsignetsim.model.math.MathDevelopper import unevaluatedSubs
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

		self.getModelInstance().build()

	def loadReducedSystem(self):
		# self.getModelInstance().buildReducedModel()
		pass
	def loadSystemComponents(self):
		t1 = time()

		function_subs = {}
		symbol_names = {}
		for variable in self.getModelInstance().getMathModel().listOfVariables.values():

			is_concentration = False
			t_symbol = variable.symbol.getDeveloppedInternalMathFormula()
			# if isinstance(t_symbol.func, SympyUndefinedFunction):
			# 	t_suffix = "(t)"
			# 	t_name = str(t_symbol.func)
			# 	is_concentration = (t_name.startswith('[') and t_name.endswith(']'))
			# 	if is_concentration:
			# 		t_name = t_name[1:-1]
			#
			# 	function_subs.update({t_symbol: SympySymbol(str(t_symbol.func))})
			# 	t_symbol = SympySymbol(str(t_symbol.func))
			# else:
			t_suffix = ""
			t_name = str(t_symbol)

			first = t_name.find('_', 1)
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

			if simplify(t_symbol - SympySymbol(t_name)) != SympyInteger(0):
				symbol_names.update({t_symbol: t_name})


		t2 = time()
		print "> symbols dictionnary built in %.2gs" % (t2-t1)


		self.latex_odes = []
		for ode in self.getModelInstance().getMathModel().listOfODEs:

			ode_formula = ode.getFormula(rawFormula=False)
			ode_latex = latex(unevaluatedSubs(expand(ode_formula), function_subs), mul_symbol='dot', symbol_names=symbol_names)
			self.latex_odes.append(ode_latex)

		t3 = time()
		print "> got ODEs in %.2gs" % (t3-t2)


		self.latex_conslaws = []
		for conslaw in self.getModelInstance().getMathModel().listOfConservationLaws:
			conslaw_formula = conslaw.getFormula(rawFormula=False)
			cs_latex = latex(unevaluatedSubs(expand(conslaw_formula), function_subs), mul_symbol='dot', symbol_names=symbol_names)
			self.latex_conslaws.append(cs_latex)

		t4 = time()
		print "> got conservation laws in %.2gs" % (t4-t3)


		self.latex_cfes = []
		for cfe in self.getModelInstance().getMathModel().listOfCFEs:
			cfe_formula = cfe.getFormula(rawFormula=False)
			cfe_latex = latex(unevaluatedSubs(expand(cfe_formula), function_subs), mul_symbol='dot', symbol_names=symbol_names)
			self.latex_cfes.append(cfe_latex)

		t5 = time()
		print "> got exact solutions in %.2gs" % (t5-t4)


		self.latex_daes = []
		for dae in self.getModelInstance().getMathModel().listOfDAEs:
			dae_formula = dae.getFormula(rawFormula=False)
			dae_latex = latex(unevaluatedSubs(expand(dae_formula), function_subs), mul_symbol='dot', symbol_names=symbol_names)
			self.latex_daes.append(dae_latex)

		t6 = time()
		print "> got DAEs in %.2gs" % (t6-t5)
