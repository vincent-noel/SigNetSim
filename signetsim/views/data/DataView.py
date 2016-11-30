#!/usr/bin/env python
""" DataView.py


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
from signetsim.views.HasWorkingProject import HasWorkingProject

from signetsim.models import Experiment, Condition, Observation, Treatment

class DataView(TemplateView, HasWorkingProject):

	template_name = 'data/data.html'

	def __init__(self, **kwargs):

		TemplateView.__init__(self, **kwargs)
		HasWorkingProject.__init__(self)

		self.listOfExperiments = None
		self.experimentId = None
		self.experimentName = None
		self.experimentNotes = None


	def get_context_data(self, **kwargs):

		kwargs = HasWorkingProject.get_context_data(self, **kwargs)

		kwargs['experimental_data'] = self.listOfExperiments
		kwargs['experiment_id'] = self.experimentId
		kwargs['experiment_name'] = self.experimentName
		kwargs['experiment_notes'] = self.experimentNotes
		return kwargs


	def get(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)
		self.loadExperiments(request)
		return TemplateView.get(self, request, *args, **kwargs)


	def post(self, request, *args, **kwargs):

		HasWorkingProject.load(self, request, *args, **kwargs)
		self.loadExperiments(request)

		if "action" in request.POST:

			if HasWorkingProject.isChooseProject(self, request):
				self.loadExperiments(request)

			elif request.POST['action'] == "create":
				self.newExperiment(request)

			elif request.POST['action'] == "delete":
				self.deleteExperiment(request)

			elif request.POST['action'] == "edit":
				self.editExperiment(request)

			elif request.POST['action'] == "save":
				self.saveExperiment(request)

			elif request.POST['action'] == "duplicate":
				self.duplicateExperiment(request)

		return TemplateView.get(self, request, *args, **kwargs)


	def loadExperiments(self, request):

		self.listOfExperiments = Experiment.objects.filter(project=self.project)


	def newExperiment(self, request):

		new_exp = Experiment(project=self.project,
							 name=request.POST['experiment_name'],
							 notes=request.POST['experiment_notes'])
		new_exp.save()



	def deleteExperiment(self, request):

		experiment = Experiment.objects.get(project=self.project,
											id=request.POST['id'])

		conditions = Condition.objects.filter(experiment=experiment)
		for condition in conditions:
			initial_data = Treatment.objects.filter(condition=condition)
			initial_data.delete()

			observed_data = Observation.objects.filter(condition=condition)
			observed_data.delete()

		conditions.delete()
		experiment.delete()


	def editExperiment(self, request):

		t_experiment = Experiment.objects.get(project=self.project,
											  id=request.POST['id'])
		self.experimentId = t_experiment.id
		self.experimentName = t_experiment.name
		self.experimentNotes = t_experiment.notes


	def saveExperiment(self, request):

		t_experiment = Experiment.objects.get(project=self.project,
											  id=request.POST['id'])

		t_experiment.name = str(request.POST['experiment_name'])
		t_experiment.notes = str(request.POST['experiment_notes'])
		t_experiment.save()


	def duplicateExperiment(self, request):
		t_experiment = Experiment.objects.get(project=self.project,
											  id=request.POST['id'])

		new_experiment = Experiment(project=self.project)
		new_experiment.save()

		t_conditions = Condition.objects.filter(experiment=t_experiment)
		for t_condition in t_conditions:

			new_condition = Condition(experiment=new_experiment)

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
				new_treatment = Treatment(
									condition=new_condition,
									species=t_treatment.species,
									time=t_treatment.time,
									value=t_treatment.value)

				new_treatment.save()

			new_condition.name = t_condition.name
			new_condition.notes = t_condition.notes

			new_condition.save()


		new_experiment.name = t_experiment.name
		new_experiment.notes = t_experiment.notes

		new_experiment.save()
