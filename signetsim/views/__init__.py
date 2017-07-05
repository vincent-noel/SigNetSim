#!/usr/bin/env python
""" __init__.py


	Initialization of the module web/signetsim/views


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

from data import DataView, ExperimentView, ConditionView

from edit import ModelCompartmentsView, ModelOverviewView, ModelOverviewView_v2
from edit import ModelParametersView, ModelReactionsView, ModelRulesView, ModelSpeciesView
from edit import ModelUnitsView, ModelEventsView, ModelMiscView, ModelSubmodelsView, ModelAnnotationsView

from simulate import TimeSeriesSimulationView, SteadyStateSimulationView, ListOfSimulationsView, SedmlSimulationView

from fit import ListOfOptimizationsView, OptimizationResultView, DataOptimizationView, DataOptimizationView0
from fit import ModelOptimizationView

from analyse import AnalyseMainView, AnalyseSensitivityView, AnalyseBifurcationsView

# from graphs import TimeseriesGraph
# from graphs import SteadyStatesGraph
# from graphs import TimeseriesOptimizationGraph
# from graphs import SteadyStatesOptimizationGraph
# from graphs import OptimizationScoreGraph
# from graphs import ObservationGraph
# from graphs import TreatmentGraph


from SuccessView import SuccessView
from HelpView import HelpView
from ListOfModelsView import ListOfModelsView
from ListOfProjectsView import ListOfProjectsView
from GenerateCombineArchive import GenerateCombineArchive

from auth import SignUpView, SignUpSuccessView, ValidateEmailView
from auth import ActivateAccountView, LoginView, ProfileView

from admin import AdminView
