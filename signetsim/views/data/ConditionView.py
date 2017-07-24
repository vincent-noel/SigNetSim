#!/usr/bin/env python
""" ConditionView.py


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


from django.shortcuts import redirect
from django.views.generic import TemplateView
from signetsim.views.HasWorkingProject import HasWorkingProject
from signetsim.views.data.ObservationForm import ObservationForm
from signetsim.views.data.TreatmentForm import TreatmentForm

from signetsim.models import Experiment, Condition, Observation, Treatment


class ConditionView(TemplateView, HasWorkingProject):

	template_name = 'data/condition.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingProject.__init__(self)

		self.experiment = None
		self.condition = None
		self.dataPoints = None
		self.treatmentPoints = None


		self.observations = None
		self.treatments = None

		self.observationForm = ObservationForm(self)
		self.treatmentForm = TreatmentForm(self)


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingProject.get_context_data(self, **kwargs)

		kwargs['experiment_name'] = self.experiment.name
		kwargs['condition_name'] = self.condition.name
		kwargs['experiment_id'] = self.experiment.id
		kwargs['experiment_data'] = self.dataPoints
		kwargs['experiment_initial_data'] = self.treatmentPoints


		kwargs['observations'] = self.observations
		kwargs['treatments'] = self.treatments


		kwargs['observation_form'] = self.observationForm
		kwargs['treatment_form'] = self.treatmentForm

		kwargs['colors'] = ['#009ece', '#ff9e00', '#9ccf31', '#f7d708', '#ce0000', '#e400ff']

		return kwargs


	def get(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		self.load(request, *args, **kwargs)

		if "action" in request.POST:

			if HasWorkingProject.isChooseProject(self, request):
				return redirect('experimental_data')
				# self.load(request, *args, **kwargs)

			elif request.POST['data_type'] == 'treatment':

				if request.POST['action'] == "delete":
					self.deleteTreatment(request)

				elif request.POST['action'] == "edit":
					self.editTreatment(request)

				elif request.POST['action'] == "save":
					self.saveTreatment(request)

				self.loadTreatments()

			elif request.POST['data_type'] == "observation":

				if request.POST['action'] == "delete":
					self.deleteObservation(request)

				elif request.POST['action'] == "edit":
					self.editObservation(request)

				elif request.POST['action'] == "save":
					print "saving observation"
					self.saveObservation(request)

				self.loadObservations()


		return TemplateView.get(self, request, *args, **kwargs)

	def load(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)

		self.loadExperiment(request, *args)
		self.loadCondition(request, *args)
		self.loadObservations()
		self.loadTreatments()


	def saveObservation(self, request):

		self.observationForm.read(request)
		if not self.observationForm.hasErrors():
			self.observationForm.save()
		else:
			self.observationForm.printErrors()

	def editObservation(self, request):
		self.observationForm.load(request)


	def deleteObservation(self, request):

		self.observationForm.read(request)
		if not self.observationForm.isNew():
			observation = Observation.objects.get(condition=self.condition,
												id=self.observationForm.id)
			observation.delete()



	def saveTreatment(self, request):

		self.treatmentForm.read(request)
		if not self.treatmentForm.hasErrors():
			self.treatmentForm.save()


	def editTreatment(self, request):
		self.treatmentForm.load(request)


	def deleteTreatment(self, request):

		self.treatmentForm.read(request)
		if not self.treatmentForm.isNew():
			treatment = Treatment.objects.get(condition=self.condition,
												id=self.treatmentForm.id)
			treatment.delete()


	def loadExperiment(self, request, *args):

		self.experiment = Experiment.objects.get(id=args[0])


	def loadCondition(self, request, *args):

		self.condition = Condition.objects.get(id=args[1])


	def loadObservations(self):

		self.dataPoints = Observation.objects.filter(condition=self.condition).order_by('time')

		list_vars = list(set([obs.species for obs in self.dataPoints]))

		self.observations = []

		for var in list_vars:
			list_obs = Observation.objects.filter(condition=self.condition, species=var).order_by('time')
			list_vals = []
			for obs in list_obs:
				list_vals.append((obs.time/60, obs.value))

			self.observations.append((str(var), list_vals))

	def loadTreatments(self):

		self.treatmentPoints = Treatment.objects.filter(condition=self.condition).order_by('time')

		list_vars = list(set([obs.species for obs in self.treatmentPoints]))

		self.treatments = []

		for var in list_vars:
			list_obs = Treatment.objects.filter(condition=self.condition, species=var).order_by('time')
			list_vals = []
			for obs in list_obs:
				list_vals.append((obs.time, obs.value))

			self.treatments.append((str(var), list_vals))
