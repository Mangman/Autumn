#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from copy import deepcopy

hash_counter = {}

#  Binary node
class Node :
	def __init__ (self) :
		raise NotImplemented

	def get_children (self) :
		raise NotImplemented

class SingleChildNode (Node) :
	_child_name = "none"

	def __init__ (self, child_name) :
		self._child_name = child_name

	def __str__ (self) :
		return "{}".format(self._child_name)

	def __repr__ (self) :
		return "{}".format(self._child_name)

	def  get_children(self) :
		return _child_id

class TwoChildNode(Node):
	_children = tuple() 
	_distances = tuple()

	def __init__(self, first_child, second_child, first_distance, second_distance):
		self._children = (deepcopy(first_child), deepcopy(second_child))
		self._distances = (first_distance, second_distance)

	def __str__ (self) :
		return "({}:{}, {}:{})".format(self._children[0], self._distances[0], self._children[1], self._distances[1])

	def __repr__ (self) :
		return "({}:{}, {}:{})".format(self._children[0], self._distances[0], self._children[1], self._distances[1])

	def get_children(self) :
		return _children