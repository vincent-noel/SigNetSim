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

""" tags.py

	This file...

"""

from django import template

register = template.Library()

@register.filter
def my_lookup(d, key):

	if d is None or key is None:
		return ""

	elif (isinstance(d, dict) and key in d) or (isinstance(d, list) and key < len(d)):
		return d[key]

	else:
		return ""

@register.filter
def get_color(d, key):
	return d[(key % len(d))]

@register.filter
def my_index(array, element):
	return array.index(element)

@register.filter
def my_len(array):
	return len(array)

@register.filter
def max_value(array):
	return max(array)

@register.filter
def min_value(array):
	return min(array)

@register.filter
def my_tuple_lookup(d, (arg1, arg2)):
	return d[(arg1, arg2)]


@register.filter
def my_model_color(array, i):
	return array[i*2]

@register.filter
def my_data_color(array, i):
	return array[i*2+1]

@register.filter
def multiply(value, multiplier):
	# you would need to do any localization of the result here
	return value * multiplier

@register.filter
def if_none(value, return_if_none):
	if value is None:
		return return_if_none
	else:
		return value