#!/usr/bin/env python
""" ExperimentView.py


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

from signetsim.models import Experiment, Condition, Observation, Treatment
from django.shortcuts import redirect
from django.views.generic import TemplateView
from signetsim.views.HasWorkingProject import HasWorkingProject

class ExperimentView(TemplateView, HasWorkingProject):

	template_name = 'data/experiment.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingProject.__init__(self)

		self.experiment = None
		self.listOfConditions = None
		self.conditionId = None
		self.conditionName = None
		self.conditionNotes = None


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingProject.get_context_data(self, **kwargs)

		kwargs['experiment_name'] = self.experiment.name
		kwargs['conditions'] = self.listOfConditions

		kwargs['condition_id'] = self.conditionId
		kwargs['condition_name'] = self.conditionName
		kwargs['condition_notes'] = self.conditionNotes

		return kwargs


	def get(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)

		self.load(request, *args, **kwargs)

		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)

		self.load(request, *args, **kwargs)

		if "action" in request.POST:

			if HasWorkingProject.isChooseProject(self, request):
				return redirect('experimental_data')

			elif request.POST['action'] == "create":
				self.newCondition(request)

			elif request.POST['action'] == "delete":
				self.deleteCondition(request)

			elif request.POST['action'] == "edit":
				self.editCondition(request)

			elif request.POST['action'] == "save":
				self.saveCondition(request)

			elif request.POST['action'] == "duplicate":
				self.duplicateCondition(request)

		return TemplateView.get(self, request, *args, **kwargs)


	def load(self, request, *args, **kwargs):

		self.loadExperiment(request, *args, **kwargs)
		self.loadConditions(request)


	def saveCondition(self, request):

		condition = Condition.objects.get(experiment=self.experiment,
										  id=request.POST['id'])

		condition.name = str(request.POST['condition_name'])
		condition.notes = str(request.POST['condition_notes'])
		condition.save()


	def editCondition(self, request):

		condition = Condition.objects.get(experiment=self.experiment,
										  id=request.POST['id'])

		self.conditionId = condition.id
		self.conditionName = condition.name
		self.conditionNotes = condition.notes


	def deleteCondition(self, request):

		condition = Condition.objects.get(experiment=self.experiment,
										  id=request.POST['id'])

		initial_data = Treatment.objects.filter(condition=condition)
		initial_data.delete()

		observed_data = Observation.objects.filter(condition=condition)
		observed_data.delete()

		condition.delete()


	def newCondition(self, request):

		new_condition = Condition(experiment=self.experiment,
								  name=request.POST['condition_name'],
								  notes=request.POST['condition_notes'])
		new_condition.save()


	def duplicateCondition(self, request):

		t_condition = Condition.objects.get(experiment=self.experiment,
											  id=request.POST['id'])

		new_condition = Condition(experiment=self.experiment)

		new_condition.save()

		t_observations = Observation.objects.filter(condition=t_condition)

		for t_observation in t_observations:
			new_observation = Observation(condition=new_condition,
								species=t_observation.species,
								time=t_observation.time,
								value=t_observation.value,
								stddev=t_observation.stddev,
								steady_state=t_observation.steady_state,
								min_steady_state=t_observation.min_steady_state,
								max_steady_state=t_observation.max_steady_state)

			new_observation.save()

		t_treatments = Treatment.objects.filter(condition=t_condition)

		for t_treatment in t_treatments:
			new_treatment = Treatment(condition=new_condition,
								species=t_treatment.species,
								time=t_treatment.time,
								value=t_treatment.value)

			new_treatment.save()

		new_condition.name = t_condition.name
		new_condition.notes = t_condition.notes

		new_condition.save()


	def loadConditions(self, request):

		self.listOfConditions = Condition.objects.filter(experiment=self.experiment)


	def loadExperiment(self, request, *args, **kwargs):

		self.experiment = Experiment.objects.get(id=args[0])
