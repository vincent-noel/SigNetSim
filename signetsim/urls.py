#!/usr/bin/env python
""" urls.py


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

from django.conf.urls import include, url
from django.contrib.auth.views import logout
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from views import HelpView, SuccessView
from views import DataView, ExperimentView, ConditionView

from views import ModelCompartmentsView, ModelOverviewView
from views import ModelSpeciesView, ModelParametersView
from views import ModelReactionsView, ModelRulesView, ModelSubmodelsView
from views import ModelUnitsView, ModelEventsView, ModelMiscView

from views import ListOfOptimizationsView, OptimizationResultView
from views import DataOptimizationView, DataOptimizationView0, ModelOptimizationView

from views import TimeSeriesSimulationView, SteadyStateSimulationView
from views import ListOfSimulationsView
from views import ListOfModelsView, ListOfProjectsView

from views import AnalyseMainView, AnalyseSensitivityView, AnalyseBifurcationsView

from views import MathValidator, SbmlIdValidator, UnitIdValidator
from views import GetSubmodels, GetListOfObjects, GetContinuationStatus
from views import GetContinuationFigure, GetListOfObjectsFromSubmodels
from views import SignUpView, SignUpSuccessView, ValidateEmailView
from views import LoginView, ActivateAccountView, ProfileView, AdminView

urlpatterns = [

	url(r'^admin_db/', include(admin.site.urls)),

	# Basic
	url(r'^$', ListOfProjectsView.as_view(), name='home'),
	url(r'^help/$', HelpView.as_view(), name='help'),
	url(r'^success/$', SuccessView.as_view(), name='success'),
	url(r'^profile/(.*)/$', ProfileView.as_view(), name='profile'),
	url(r'^admin/$', AdminView.as_view(), name='admin'),

	# Model import/export
	url(r'^project/([^/]+)/$', ListOfModelsView.as_view(), name='project'),
	url(r'^models/$', ListOfModelsView.as_view(), name='models'),

	# Authentication
	url(r'^accounts/register/$', SignUpView.as_view(), name='signup'),
	url(r'^accounts/register_success/$', SignUpSuccessView.as_view(), name='signup_success'),
	url(r'^accounts/login/$', LoginView.as_view(), name='login'),
	url(r'^accounts/logout/$',  logout, {'next_page': 'login'}, name='logout'),
	url(r'^accounts/validate_email/', ValidateEmailView.as_view(), name='validate_email'),
	url(r'^accounts/activate_account/', ActivateAccountView.as_view(), name='activate_account'),

	# Model editing
	url(r'^edit/model/([^/]+)/$', ModelOverviewView.as_view(), name='edit_model'),
	url(r'^edit/overview/$', ModelOverviewView.as_view(), name='edit_overview'),
	url(r'^edit/species/$', ModelSpeciesView.as_view(), name='edit_species'),
	url(r'^edit/parameters/$', ModelParametersView.as_view(), name='edit_parameters'),
	url(r'^edit/reactions/$', ModelReactionsView.as_view(), name='edit_reactions'),
	url(r'^edit/rules/$', ModelRulesView.as_view(), name='edit_rules'),
	url(r'^edit/events/$', ModelEventsView.as_view(), name='edit_events'),
	url(r'^edit/units/$', ModelUnitsView.as_view(), name='edit_units'),
	url(r'^edit/compartments/$', ModelCompartmentsView.as_view(), name='edit_compartments'),
	url(r'^edit/misc/$', ModelMiscView.as_view(), name='edit_misc'),
	url(r'^edit/submodels/$', ModelSubmodelsView.as_view(), name='edit_submodels'),

	# Simulation
	url(r'^simulate/timeseries/$', TimeSeriesSimulationView.as_view(), name='simulate_model'),
	url(r'^simulate/steady_states/$', SteadyStateSimulationView.as_view(), name='simulate_steady_states'),
	url(r'^simulate/stored/$', ListOfSimulationsView.as_view(), name='list_of_simulations'),

	# Optimization
	url(r'^fit/model/$', ModelOptimizationView.as_view(), name='optimize_model'),
	url(r'^fit/data/$', DataOptimizationView0.as_view(), name='optimize_data'),
	url(r'^fit/list/$', ListOfOptimizationsView.as_view(), name='list_of_optimizations'),
	url(r'^fit/([0-9]+)/$', OptimizationResultView.as_view(), name='view_optimization'),

	# Experimental data
	url(r'^data/$', DataView.as_view(), name='experimental_data'),
	url(r'^data/([^/]+)/$', ExperimentView.as_view(), name='experiment'),
	url(r'^data/([^/]+)/([^/]+)/$', ConditionView.as_view(), name='experiment_data'),

	# Analyses
	url(r'^analyse/$', AnalyseMainView.as_view(), name='analyse'),
	url(r'^analyse/sensitivity/$', AnalyseSensitivityView.as_view(), name='sensitivity'),
	url(r'^analyse/bifurcations/$', AnalyseBifurcationsView.as_view(), name='bifurcations'),

	# JSON requests
	url(r'^json/math_validator/$', MathValidator.as_view(), name='math_validator'),
	url(r'^json/sbml_id_validator/$', SbmlIdValidator.as_view(), name='sbml_id_validator'),
	url(r'^json/unit_id_validator/$', UnitIdValidator.as_view(), name='unit_id_validator'),
	url(r'^json/get_submodels/$', GetSubmodels.as_view(), name='get_submodels'),
	url(r'^json/get_list_of_objects/$', GetListOfObjects.as_view(), name='get_list_of_objects'),
	url(r'^json/get_list_of_objects_from_submodels/$', GetListOfObjectsFromSubmodels.as_view(), name='get_list_of_objects_from_submodels'),

	url(r'^json/get_continuation_status/$', GetContinuationStatus.as_view(), name='get_continuation_status'),
	url(r'^json/get_continuation_figure/$', GetContinuationFigure.as_view(), name='get_continuation_figure'),


]

if settings.SIGNETSIM_MODE == 'development':
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)