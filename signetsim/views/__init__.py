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

""" __init__.py

	Initialization of the module web/signetsim/views

"""

from .data import DataView, ExperimentView, ConditionView, DataArchive

from .edit import ModelCompartmentsView, ModelOverviewView
from .edit import ModelParametersView, ModelReactionsView, ModelRulesView, ModelSpeciesView
from .edit import ModelUnitsView, ModelEventsView, ModelMiscView, ModelSubmodelsView, ModelAnnotationsView

from .simulate import TimeSeriesSimulationView, SteadyStateSimulationView, PhasePlaneSimulationView
from .simulate import ListOfSimulationsView, SedmlSimulationView

from .fit import ListOfOptimizationsView, OptimizationResultView, DataOptimizationView
from .fit import ModelOptimizationView

from .analyse import AnalyseMainView, AnalyseSensitivityView, AnalyseBifurcationsView

from .SuccessView import SuccessView
from .HelpView import HelpView
from .InstallView import InstallView
from .ListOfModelsView import ListOfModelsView
from .ListOfProjectsView import ListOfProjectsView
from .ProjectArchive import ProjectArchive
from .SimulationArchive import SimulationArchive

from .auth import SignUpView, SignUpSuccessView, ValidateEmailView
from .auth import ActivateAccountView, LoginView, ProfileView

from .admin import AdminView
