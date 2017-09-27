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
from signetsim.models import ContinuationComputation, SbmlModel
from signetsim.views.HasWorkingModel import HasWorkingModel
from signetsim.views.analyse.AnalyseBifurcationForm import AnalyseBifurcationsForm
import dill, mpld3
from matplotlib import pyplot as plt

class AnalyseBifurcationsView(TemplateView, HasWorkingModel, HasErrorMessages):

	template_name = 'analyse/bifurcations.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)
		HasErrorMessages.__init__(self)

		self.listOfConstants = None
		self.listOfVariables = None
		self.listComputations = None
		self.listOfFigures = None
		self.computation = None

		self.form = AnalyseBifurcationsForm(self)


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)
		kwargs['list_of_constants'] = [const.getNameOrSbmlId() for const in self.listOfConstants]
		kwargs['list_of_variables'] = [var.getNameOrSbmlId() for var in self.listOfVariables]
		kwargs['list_of_computations'] = self.listOfComputations
		kwargs['list_of_figures'] = self.listOfFigures
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
		t_computation = ContinuationComputation.objects.get(id=curve_id)
		t_computation.delete()

	def callback_success(self, code):
		self.computation.figure = dill.dumps(code).decode('Latin-1')
		self.computation.status = ContinuationComputation.ENDED
		self.computation.save()

	def callback_error(self):
		self.computation.figure = ""
		self.computation.status = ContinuationComputation.ERROR
		self.computation.save()


	def load(self, request, *args, **kwargs):
		HasWorkingModel.load(self, request, *args, **kwargs)
		HasErrorMessages.clearErrors(self)
		self.loadConstants()
		self.loadComputations()
		self.loadFigures()


	def loadConstants(self):
		self.getModelInstance().listOfVariables.classifyVariables()
		self.listOfConstants = [variable for variable in self.getModel().listOfVariables.values() if variable.isConstant() or variable.isDerivative()]
		self.listOfVariables = [variable for variable in self.getModel().listOfVariables.values() if variable.isDerivative()]


	def loadComputations(self):

		t_model = SbmlModel.objects.get(project=self.project_id, id=self.model_id)
		self.listOfComputations = ContinuationComputation.objects.filter(project=self.project, model=t_model)


	def loadFigures(self):

		self.listOfFigures = []
		for continuation in self.listOfComputations:
			if continuation.figure is not None:# and str(continuation.figure) != "":
				# print len(str(continuation.figure))
				try:

					t_object = dill.loads(continuation.figure.encode('Latin-1'))
					t_object.continuation.plot.setLabels('')
					t_object.continuation.plot.toggleLabels(visible="on")
					t_object.continuation.display((t_object.parameter, t_object.variable), stability=True,linewidth=3,
											color='#009ece',)

					t_figure_id = plt.get_fignums()[0]
					t_figure = plt.figure(t_figure_id)

					t_figure.get_axes()[0].set_title("")
					t_figure.get_axes()[0].set_xlim([t_object.fromValue, t_object.toValue])

					t_figure.set_dpi(100)
					t_figure.set_size_inches((8, 5))

					t_figure_html = mpld3.fig_to_html(t_figure, template_type='simple')
					t_figure_html = t_figure_html.replace(
						"<script type=\"text/javascript\" src=\"https://mpld3.github.io/js/d3.v3.min.js\"></script>", "")
					t_figure_html = t_figure_html.replace(
						"<script type=\"text/javascript\" src=\"https://mpld3.github.io/js/mpld3.v0.3.js\"></script>", "")
					t_figure_html = t_figure_html.replace("<style>", "")
					t_figure_html = t_figure_html.replace("</style>", "")
					self.listOfFigures.append(t_figure_html)
				except:
					self.listOfFigures.append("")

			else:
				self.listOfFigures.append("")

	def computeCurve(self, request):

		self.form.read(request)
		if not self.form.hasErrors():


			t_model = SbmlModel.objects.get(project=self.project_id, id=self.model_id)

			self.computation = ContinuationComputation(project=self.project,
													   model=t_model,
													   parameter=self.listOfConstants[self.form.parameter].getSbmlId(),
													   variable=self.listOfVariables[self.form.variable].getSbmlId())#,
													   # ds=ds, max_steps=max_steps)
			self.computation.save()

			if self.form.parameter is not None and self.form.variable is not None:

				t_ep_curve = EquilibriumPointCurve(self.getModel())
				t_ep_curve.setParameter(self.listOfConstants[self.form.parameter])
				t_ep_curve.setVariable(self.listOfVariables[self.form.variable].getSbmlId())
				t_ep_curve.setRange(self.form.fromValue, self.form.toValue)
				t_ep_curve.setDs(self.form.ds)
				t_ep_curve.setMaxSteps(self.form.maxSteps)
				t_ep_curve.build()
				t_ep_curve.run(self.callback_success, self.callback_error)
