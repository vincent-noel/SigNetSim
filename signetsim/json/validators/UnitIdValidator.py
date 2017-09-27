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

""" UnitIdValidator.py

	This file...

"""

from libsbml import SyntaxChecker

from signetsim.json import JsonRequest
from signetsim.views.HasWorkingModel import HasWorkingModel


class UnitIdValidator(JsonRequest, HasWorkingModel):

    def __init__(self):
        JsonRequest.__init__(self)
        HasWorkingModel.__init__(self)


    def post(self, request, *args, **kwargs):
        self.load(request, *args, **kwargs)

        unit_id = str(request.POST['unit_id'])

        if not self.getModel().listOfUnitDefinitions.isUnitIdAvailable(unit_id):
            self.data.update({'valid': 'false'})

        elif not SyntaxChecker.isValidUnitSId(unit_id):
            self.data.update({'valid': 'false'})

        else:
            self.data.update({'valid': 'true'})

        return JsonRequest.post(self, request, *args, **kwargs)


    def load(self, request, *args, **kwargs):
        HasWorkingModel.load(self, request, *args, **kwargs)