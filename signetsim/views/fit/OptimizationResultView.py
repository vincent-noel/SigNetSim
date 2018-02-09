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

""" OptimizationResultView.py

	This file ...

"""

from django.core.files import File
from django.conf import settings
from django.shortcuts import redirect

from signetsim.models import SbmlModel
import os
import re
from threading import Thread
from time import sleep

from django.views.generic import TemplateView
from signetsim.views.HasWorkingProject import HasWorkingProject
from libsignetsim.model.SbmlDocument import SbmlDocument
from signetsim.settings.Settings import Settings
from signetsim.managers.optimizations import getOptimizationStatus, stopOptimization, restartOptimization


class OptimizationResultView(TemplateView, HasWorkingProject):

		template_name = 'fit/result.html'

		def __init__(self, **kwargs):

			TemplateView.__init__(self, **kwargs)
			HasWorkingProject.__init__(self)

			self.optimizationId = None

			self.parameters = None
			self.inputParameters = None
			self.outputParameters = None

			self.modelName = None
			self.submodelNames = None
			self.modifiedSubmodelNames = None
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

			self.optimizationModel = None


		def get_context_data(self, **kwargs):

			kwargs = HasWorkingProject.get_context_data(self, **kwargs)

			kwargs['optimization_id'] = self.optimizationId
			kwargs['parameters'] = self.parameters
			kwargs['model_name'] = self.modelName
			kwargs['submodel_names'] = self.submodelNames
			kwargs['modified_submodel_names'] = self.modifiedSubmodelNames
			kwargs['show_graph'] = self.showGraph
			kwargs['optimization_status'] = self.optimizationStatus

			kwargs['score_time'] = self.scoreTime
			kwargs['score_values'] = self.scoreValues
			kwargs['score_rawvalues'] = self.scoreRawValues
			kwargs['score_minev'] = self.scoreMinEv
			kwargs['score_maxev'] = self.scoreMaxEv
			kwargs['colors'] = Settings.default_colors

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
					self.saveFittedModel(request)

				elif request.POST['action'] == "stop_optim":
					self.stopOptimization()

				elif request.POST['action'] == "restart_optim":
					self.restartOptimization()

			return TemplateView.get(self, request, *args, **kwargs)

		def load(self, request, *args, **kwargs):

			HasWorkingProject.load(self, request, *args, **kwargs)

			if self.isProjectLoaded():
				self.loadOptimization(request, *args)


		def stopOptimization(self):

			stopOptimization(self.optimPath)
			self.optimizationStatus = getOptimizationStatus(self.optimPath)


		def restartOptimization(self):

			t = Thread(
				group=None,
				target=restartOptimization,
				args=(self.optimPath,)
			)

			t.setDaemon(True)
			t.start()
			sleep(2)

			self.optimizationStatus = getOptimizationStatus(self.optimPath)

		def saveFittedModel(self, request):

			t_document = SbmlDocument()
			t_document.readSbmlFromFile(str(self.optimPath + "/model.sbml"))
			model = t_document.model

			if request.POST.get('model_name') is not None:
				self.modelName = str(request.POST['model_name'])
			elif model.getName() is not None:
				self.modelName = model.getName()
			else:
				self.modelName = self.model_name

			if not SbmlModel.objects.filter(name=self.modelName):

				document = SbmlDocument()
				document.readSbmlFromFile(os.path.join(settings.MEDIA_ROOT, os.path.join(self.optimPath, "model.sbml")))

				if not document.useCompPackage:

					file = File(open(os.path.join(settings.MEDIA_ROOT, os.path.join(self.optimPath, "model.sbml"))))
					new_sbml_model = SbmlModel(project=self.project, name=self.modelName, sbml_file=file)
					new_sbml_model.save()

					new_document = SbmlDocument()
					new_document.readSbmlFromFile(os.path.join(settings.MEDIA_ROOT, str(new_sbml_model.sbml_file)))
					new_document.model.setName(self.modelName)

					for i_param, (xpath, value) in enumerate(self.outputParameters):

						param = new_document.getByXPath(xpath)
						param.setValue(value)

					new_document.writeSbmlToFile(os.path.join(settings.MEDIA_ROOT, str(new_sbml_model.sbml_file)))

				else:
					modifieds = []
					for i_param, (xpath, value) in enumerate(self.outputParameters):
						param = document.getModelInstance().getDefinitionVariableByXPath(xpath)
						modifieds.append(param[0].getModel().parentDoc)

					modifieds = list(set(modifieds))

					submodel_names = []
					i_submodel = 0
					while request.POST.get("submodel_%d_name" % i_submodel) is not None:
						submodel_names.append(request.POST["submodel_%d_name" % i_submodel])
						i_submodel += 1

					modified_files = {}
					for i_modified, modified in enumerate(modifieds):
						file = File(open(os.path.join(settings.MEDIA_ROOT, os.path.join(self.optimPath, modified.documentFilename))))
						new_sbml_model = SbmlModel(project=self.project, name=submodel_names[i_modified], sbml_file=file)
						new_sbml_model.save()

						new_document = SbmlDocument()
						new_document.readSbmlFromFile(os.path.join(settings.MEDIA_ROOT, str(new_sbml_model.sbml_file)))
						new_document.model.setName(str(submodel_names[i_modified]))
						new_document.writeSbmlToFile(os.path.join(settings.MEDIA_ROOT, str(new_sbml_model.sbml_file)))
						modified_files.update({modified.documentFilename: os.path.basename(str(new_sbml_model.sbml_file))})

					print modified_files
					print [subdoc.documentFilename for subdoc in document.documentDependencies]
					renaming = {}
					for subdoc in document.documentDependencies:
						if subdoc.documentFilename in modified_files:
							renaming.update({subdoc.documentFilename: modified_files[subdoc.documentFilename]})
						else:
							renaming.update({subdoc.documentFilename: subdoc.documentFilename})

					print renaming

					file = File(open(os.path.join(settings.MEDIA_ROOT, os.path.join(self.optimPath, "model.sbml"))))
					new_sbml_model = SbmlModel(project=self.project, name=self.modelName, sbml_file=file)
					new_sbml_model.save()

					new_document = SbmlDocument()
					new_document.readSbmlFromFile(os.path.join(settings.MEDIA_ROOT, str(new_sbml_model.sbml_file)))
					new_document.renameExternalDocumentDependencies(renaming)
					new_document.model.setName(self.modelName)
					new_document.writeSbmlToFile(os.path.join(settings.MEDIA_ROOT, str(new_sbml_model.sbml_file)))

		def loadOptimization(self, request, *args):

			self.optimizationId = str(args[0])
			self.optimPath = os.path.join(self.getProjectFolder(),
							"optimizations/optimization_%s/" % self.optimizationId)

			self.optimizationStatus = getOptimizationStatus(self.optimPath)

			self.showGraph = None
			self.parameters = []
			self.loadOptimizationResults(request)
			self.loadOptimizationScore(request)
			self.readModel(request)
			self.loadParameters(request)
			self.loadSubmodels(request)
			request.session['optim_dir'] = self.optimPath
			request.session['logdir'] = os.path.join(self.optimPath, "logs")



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

		def loadParameters(self, request):


			self.inputParameters = []
			self.outputParameters = []

			if os.path.isfile(os.path.join(self.optimPath, "logs/params/input")):
				f_input = open(os.path.join(self.optimPath, "logs/params/input"))

				for line in f_input:
					res = re.split(" ", line.strip())
					xpath = res[0]
					value = res[2]
					self.inputParameters.append((xpath, value))

			if os.path.isfile(os.path.join(self.optimPath, "logs/params/output")):
				f_input = open(os.path.join(self.optimPath, "logs/params/output"))

				for line in f_input:
					res = re.split(" ", line.strip())
					xpath = res[0]
					value = res[2]
					self.outputParameters.append((xpath, value))

			elif os.path.isfile(os.path.join(self.optimPath, "logs/best_res/parameters_0")):
				f_input = open(os.path.join(self.optimPath, "logs/best_res/parameters_0"))

				for line in f_input:
					res = re.split(" ", line.strip())
					xpath = res[0]
					value = res[2]
					self.outputParameters.append((xpath, value))

			if len(self.inputParameters) > 0 and len(self.outputParameters) == len(self.inputParameters):
				self.parameters = []
				for i, (xpath, value) in enumerate(self.inputParameters):
					parameter = self.optimizationModel.getByXPath(xpath, instance=self.optimizationModel.useCompPackage)
					self.parameters.append((parameter.getNameOrSbmlId(), value, self.outputParameters[i][1]))

		def loadSubmodels(self, request):


			if self.optimizationModel.useCompPackage:
				self.optimizationModel.loadExternalDocumentDependencies()

				self.modifiedSubmodelNames = {}
				for subdoc in self.optimizationModel.documentDependencies:
					self.modifiedSubmodelNames[subdoc.model.getNameOrSbmlId()] = False

				for i_param, (xpath, value) in enumerate(self.outputParameters):
					param = self.optimizationModel.getModelInstance().getDefinitionVariableByXPath(xpath)

					self.modifiedSubmodelNames[param[0].getModel().getName()] = True

				self.submodelNames = []
				for subdoc in self.optimizationModel.documentDependencies:
					if self.modifiedSubmodelNames[subdoc.model.getNameOrSbmlId()]:
						if subdoc.model.getNameOrSbmlId() is None:
							self.submodelNames.append("")
						else:
							self.submodelNames.append(subdoc.model.getNameOrSbmlId())


		def readModel(self, request):

			self.optimizationModel = SbmlDocument()
			self.optimizationModel.readSbmlFromFile(os.path.join(self.optimPath, "model.sbml"))
			if self.optimizationModel.getModelInstance().getNameOrSbmlId() is not None:
				self.modelName = self.optimizationModel.getModelInstance().getNameOrSbmlId()
			else:
				self.modelName = self.optimizationModel.model.getNameOrSbmlId()
