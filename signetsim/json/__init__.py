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

	Initialization of the module web/signetsim

"""

from JsonRequest import JsonRequest

from admin import SetAccountStaff, SetAccountActive
from data import GetExperiment, GetCondition, GetTreatment, GetObservation
from edit import GetListOfObjects, GetListOfObjectsFromSubmodels
from edit import GetSpecies, GetParameter, GetCompartment, GetReaction, GetReactionKineticLaw, GetRule, \
	GetEvent, GetSubmodel, GetSubstitution, GetSubmodels, GetSBOName, GetUnitDefinition
from validators import FloatValidator, MathValidator, SbmlIdValidator, UnitIdValidator, ModelNameValidator
from fit import AddDataset
from analyse import GetEquilibriumCurve, GetContinuationStatus
from GetProject import GetProject
from SearchBiomodels import SearchBiomodels
from GetBiomodelsName import GetBiomodelsName
from GetInstallStatus import GetInstallStatus
