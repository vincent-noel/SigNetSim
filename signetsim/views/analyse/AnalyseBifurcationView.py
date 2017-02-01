#!/usr/bin/env python
""" AnalyseBifurcationView.py


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

from libsignetsim.continuation.EquilibriumPointCurve import EquilibriumPointCurve
from django.views.generic import TemplateView
from signetsim.views.HasErrorMessages import HasErrorMessages
from django.core.urlresolvers import reverse
from signetsim.models import ContinuationComputation, SbmlModel

from libsignetsim.settings.Settings import Settings
import pickle
import threading
# from signetsim.models import SbmlModel
from signetsim.views.HasWorkingModel import HasWorkingModel
class AnalyseBifurcationsView(TemplateView, HasWorkingModel, HasErrorMessages):

	template_name = 'analyse/bifurcations.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingModel.__init__(self)
		HasErrorMessages.__init__(self)

		self.listOfConstants = None
		self.listOfVariables = None
		self.listComputations = None
		self.computation = None

	def get_context_data(self, **kwargs):

		kwargs = HasWorkingModel.get_context_data(self, **kwargs)
		kwargs = HasErrorMessages.get_context_data(self, **kwargs)
		kwargs['list_of_constants'] = [const.getNameOrSbmlId() for const in self.listOfConstants]
		kwargs['list_of_variables'] = [var.getNameOrSbmlId() for var in self.listOfVariables]
		kwargs['list_of_computations'] = self.listOfComputations
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

		return TemplateView.get(self, request, *args, **kwargs)


	def callback_success(self, code):
		self.computation.figure = code
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


	def loadConstants(self):
		self.getModelInstance().listOfVariables.classifyVariables()
		self.listOfConstants = [variable for variable in self.getModelInstance().listOfVariables.values() if variable.isConstant() or variable.isDerivative()]
		self.listOfVariables = [variable for variable in self.getModelInstance().listOfVariables.values() if variable.isDerivative()]


	def loadComputations(self):

		t_model = SbmlModel.objects.get(project=self.project_id, id=self.model_id)
		self.listOfComputations = ContinuationComputation.objects.filter(project=self.project, model=t_model)


	def computeCurve(self, request):

		t_parameter_id = self.readInt(request, 'parameter_id', "the identifier of the parameter", required=True, max_value=len(self.listOfConstants))
		t_variable_id = self.readInt(request, 'variable_id', "the identifier of the variable", required=True, max_value=len(self.listOfVariables))
		if t_parameter_id is not None and t_variable_id is not None:
			t_ep_curve = EquilibriumPointCurve(self.getModelInstance())
			t_ep_curve.setParameter(self.listOfConstants[t_parameter_id])
			t_ep_curve.setVariable(self.listOfVariables[t_variable_id].getSbmlId())
			t_ep_curve.build()
			t_ep_curve.run(self.callback_success, self.callback_error)

		t_model = SbmlModel.objects.get(project=self.project_id, id=self.model_id)
		self.computation = ContinuationComputation(project=self.project,
									model=t_model,
									parameter=self.listOfConstants[t_parameter_id].getSbmlId(),
									variable=self.listOfVariables[t_variable_id].getSbmlId())
		self.computation.save()
