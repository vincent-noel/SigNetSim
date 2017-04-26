#!/usr/bin/env python
""" UnitIdValidator.py


	This file...



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

from signetsim.views.json.JsonView import JsonView
from signetsim.views.HasWorkingModel import HasWorkingModel
from libsbml import SyntaxChecker

class UnitIdValidator(JsonView, HasWorkingModel):

    def __init__(self):
        JsonView.__init__(self)
        HasWorkingModel.__init__(self)


    def post(self, request, *args, **kwargs):
        self.load(request, *args, **kwargs)

        unit_id = str(request.POST['unit_id'])

        if not self.model.listOfUnits.isUnitIdAvailable(unit_id):
            self.data.update({'valid': 'false'})

        elif not SyntaxChecker.isValidUnitSId(unit_id):
            self.data.update({'valid': 'false'})

        else:
            self.data.update({'valid': 'true'})

        return JsonView.post(self, request, *args, **kwargs)


    def load(self, request, *args, **kwargs):
        HasWorkingModel.load(self, request, *args, **kwargs)