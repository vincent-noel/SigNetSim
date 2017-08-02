#!/usr/bin/env python
""" OptimizationResultView.py


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

from django.core.files import File
from django.conf import settings
from django.shortcuts import redirect

from signetsim.models import SbmlModel
import os
import re

from django.views.generic import TemplateView
from signetsim.views.HasWorkingProject import HasWorkingProject

class OptimizationResultView(TemplateView, HasWorkingProject):

	template_name = 'fit/result.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingProject.__init__(self)

		self.optimizationId = None
		self.parameters = None
		self.modelName = None
		self.optimizationStatus = None
		self.showGraph = None
		self.optimPath = None

		self.experiments = None
		self.experimentsData = None

		self.scoreTime = []
		self.scoreValues = []
		self.scoreRawValues = []
		self.scoreMinEv = []
		self.scoreMaxEv = []


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingProject.get_context_data(self, **kwargs)

		kwargs['optimization_id'] = self.optimizationId
		kwargs['parameters'] = self.parameters
		kwargs['model_name'] = self.modelName
		kwargs['show_graph'] = self.showGraph
		kwargs['optimization_status'] = self.optimizationStatus

		kwargs['score_time'] = self.scoreTime
		kwargs['score_values'] = self.scoreValues
		kwargs['score_rawvalues'] = self.scoreRawValues
		kwargs['score_minev'] = self.scoreMinEv
		kwargs['score_maxev'] = self.scoreMaxEv
		kwargs['colors'] = ['#009ece', '#ff9e00', '#9ccf31', '#f7d708', '#ce0000', '#e400ff']

		#kwargs['experiments'] = self.experiments
		kwargs['experiments'] = self.experimentsData
		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:
			if HasWorkingProject.isChooseProject(self, request):
				return redirect('list_of_optimizations')

			if request.POST['action'] == "save_model":
				self.saveModel(request)

			elif request.POST['action'] == "stop_optim":
				self.stopOptimization()


		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)

		if self.isProjectLoaded():
			self.loadOptimization(request, *args)


	def saveModel(self, request):

		t_file = File(open(os.path.join(self.optimPath, "fitted_model.sbml")))

		t_model = SbmlModel.objects.get(name=self.modelName)
		t_model.sbml_file = t_file
		t_model.save()


	def stopOptimization(self):

		if os.path.isfile(os.path.join(self.optimPath, "pid")):

			t_pidfile = open(os.path.join(self.optimPath, "pid"), "r")
			t_pid = int(t_pidfile.readline().strip())
			os.kill(t_pid, 9)


	# def saveAsNewModel(self, request):
	#
	#     if not SbmlModel.objects.filter(name=("%s (fitted)" % self.modelName)):
	#
	#         t_model = FittedSbmlModel.objects.get(optimization_id=self.optimizationId)
	#         t_file = File(open(os.path.join(settings.MEDIA_ROOT, str(t_model.sbml_file))))
	#         new_sbml_model = SbmlModel(project=self.project,
	#                                     name=("%s (fitted)" % self.modelName),
	#                                     sbml_file=t_file)
	#
	#         new_sbml_model.save()

	#
	#
	# def saveFittedModel(self, request):
	#
	#     t_document = SbmlDocument()
	#     t_document.readSbml(str(self.optimPath + "/model.sbml"))
	#     model = t_document.model
	#
	#     self.modelName = model.getName()
	#
	#     # Because we want the list of constants
	#     model.listOfVariables.classifyVariables()
	#
	#     input_parameters = self.readParameters(model, self.optimPath + "/fit_input")
	#     output_parameters = self.readParameters(model, self.optimPath + "/fit_output")
	#
	#     for i_param, param in enumerate(input_parameters):
	#         (t_id_input, t_name_input, t_val_input) = param
	#         (_, _, t_val_output) = output_parameters[i_param]
	#
	#         self.parameters.append((t_id_input, t_val_input, t_val_output, t_name_input))
	#         model.variablesConstant[t_id_input].setValue(t_val_output)
	#
	#     if not FittedSbmlModel.objects.filter(optimization_id=self.optimizationId).exists():
	#         model.parentDoc.writeSbml(str(self.optimPath + "/fitted_model.sbml"))
	#         t_file = File(open(str(self.optimPath + "/fitted_model.sbml")))
	#         new_fitted_model = FittedSbmlModel(project=self.project, optimization_id=self.optimizationId, name=model.getName(), sbml_file=t_file)
	#         new_fitted_model.save()
	#     else:
	#         t_fitted_model = FittedSbmlModel.objects.get(optimization_id=self.optimizationId)
	#         model.parentDoc.writeSbml(os.path.join(settings.MEDIA_ROOT, str(t_fitted_model.sbml_file)))


	def loadOptimization(self, request, *args):


		self.optimizationId = str(args[0])
		self.optimPath = os.path.join(self.getProjectFolder(),
						"optimizations/optimization_%s/" % self.optimizationId)

		self.optimizationStatus = None

		# print self.optimPath
		# printos.path.join(self.optimPath, "/logs/score/score")
		# print os.path.isfile(os.path.join(self.optimPath, "/logs/score/score"))
		if not os.path.exists(self.optimPath):
			self.optimizationStatus = "Not found"

		elif os.path.isfile(self.optimPath + "/logs/score/score"):
			self.optimizationStatus = "Finished"

		elif os.path.getsize(self.optimPath + "/err_optim") > 0:
			self.optimizationStatus = "Interrupted"

		else:
			self.optimizationStatus = "Ongoing"

		self.showGraph = None
		self.parameters = []
		self.loadOptimizationResults(request)
		self.loadOptimizationScore(request)
		request.session['optim_dir'] = self.optimPath
		request.session['logdir'] = os.path.join(self.optimPath, "logs")
		# self.saveFittedModel(request)



	def loadOptimizationResults(self, request):

		nb_experiments = 0
		nb_conditions = 0

		self.max_conditions = 0
		self.max_vars = 0

		vars_structure = []
		data_structure = []

		while (os.path.isfile(os.path.join(self.optimPath, "logs/exp_%d_cond_%d_var_%d" % (
				nb_experiments, 0, 0)))):


			nb_conditions = 0
			t_cond_vars_structure = []
			t_cond_data_structure = []
			while (os.path.isfile(os.path.join(self.optimPath, "logs/exp_%d_cond_%d_var_0" % (nb_experiments, nb_conditions)))):

				nb_vars = 0
				t_var_data_structure = []
				while(os.path.isfile(os.path.join(self.optimPath, "logs/exp_%d_cond_%d_var_%d" % (nb_experiments, nb_conditions, nb_vars)))):
					t_var_data_structure.append((self.readModelSimulation(nb_experiments,nb_conditions, nb_vars), self.readObservation(nb_experiments, nb_conditions, nb_vars)))
					nb_vars += 1

				#print t_var_data_structure
				t_cond_vars_structure.append(nb_vars)
				t_cond_data_structure.append(t_var_data_structure)
				nb_conditions += 1
				self.max_vars = max(self.max_vars, nb_vars)

			self.max_conditions = max(self.max_conditions, nb_conditions)
			vars_structure.append(t_cond_vars_structure)
			data_structure.append(t_cond_data_structure)
			nb_experiments += 1


		#print data_structure
		self.experiments = vars_structure
		self.experimentsData = data_structure



	def readObservation(self, experiment, condition, var):

		f_optim = open(
			os.path.join(self.optimPath, "logs/exp_%d_cond_%d_var_%d" %
						 (experiment, condition, var)), "r")


		res = []
		for line in f_optim:
			data = re.split("\t", line.strip())
			res.append((float(data[0]), float(data[1]), float(data[2])))


		f_optim.close()
		return res


	def readModelSimulation(self, experiment, condition, var, proc=0):


		if os.path.isfile(os.path.join(self.optimPath,
					"logs/res/model_exp_%d_cond_%d_var_%d_proc_%d" %
					 (experiment, condition, var, proc))):

			f_optim = open(
						os.path.join(self.optimPath,
							"logs/res/model_exp_%d_cond_%d_var_%d_proc_%d" %
							 (experiment, condition, var, proc)), "r")
		elif os.path.isfile(os.path.join(self.optimPath,
					"logs/best_res/model_exp_%d_cond_%d_var_%d_proc_%d" %
					 (experiment, condition, var, proc))):

			f_optim = open(
						os.path.join(self.optimPath,
							"logs/best_res/model_exp_%d_cond_%d_var_%d_proc_%d" %
							 (experiment, condition, var, proc)), "r")

		else:
			return

		res = []

		for line in f_optim:
			data = re.split("\t", line.strip())
#            x.append(float(data[0]) / 60)
#            y.append(float(data[1]))
			res.append((float(data[0]), float(data[1])))

		f_optim.close()

		return res

	def loadOptimizationScore(self, request):

		if os.path.isfile(os.path.join(self.optimPath, "plsa.log")):

			# Reading file
			f_optim = open(os.path.join(self.optimPath, "plsa.log"), "r")

			for line in f_optim:
				data = re.split("\t", line.strip())
				self.scoreTime.append(float(data[0]))
				self.scoreValues.append(float(data[5]))
				self.scoreRawValues.append(float(data[3]))
				self.scoreMinEv.append(max(0.0, float(data[5])-float(data[6])))
				self.scoreMaxEv.append(float(data[5])+float(data[6]))




	def readParameters(self, model, filename):

		result_params = []

		f_optimized_parameters = open(filename, 'r')
		now_reading = 0

		for line in f_optimized_parameters:
			# Comments
			if line.startswith("#"):
				pass

			# Empty line
			elif not line.strip():
				pass

			# Parameter_label
			elif line.strip() == "[constants]":
				now_reading = 1
			elif line.strip() == "[initial_values]":
				now_reading = 2
			else:
				# print line
				data = line.strip().split()
				if now_reading == 1:
					t_ind = int(data[0])
					t_value = float(data[1])

					if model.variablesConstant[t_ind].isParameter():
						result_params.append((t_ind, model.variablesConstant[t_ind].getNameOrSbmlId(), t_value))

		f_optimized_parameters.close()
		return result_params
