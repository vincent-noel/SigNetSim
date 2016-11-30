#!/usr/bin/env python
""" tags.py


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
