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

""" forms.py

	This file ...

"""

from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class DocumentForm(forms.Form):
	docfile = forms.FileField(label='')

	def __init__(self, *args, **kwargs):
		super(DocumentForm, self).__init__(*args, **kwargs)
		self.fields['docfile'].widget.attrs['class'] = 'btn btn-default btn-file'
