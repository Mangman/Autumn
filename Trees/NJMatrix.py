#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from collections import defaultdict
from Node import SingleChildNode, TwoChildNode

#  Neighbor joining matrix
class NJMatrix :
	matrix = dict()
	
	def __init__ (self, reads) :
		second_names = {}

		for name in reads :
			node = SingleChildNode(name)
			second_names[name] = node
			self.matrix[node] = {}

		for first_name in reads :
			first_node = second_names[first_name]
			for second_name in reads :
				second_node = second_names[second_name]
				if first_name != second_name :
					self.matrix[first_node][second_node] = calculate_distance(reads[first_name], reads[second_name])
				else :
					self.matrix[first_node][second_node] = 0

	def join_neighbours (self) :
		while (len(self.matrix) > 3) :
			names = self._find_closest()

			first_sum = sum(self.matrix[names[0]].values())
			second_sum = sum(self.matrix[names[1]].values())
			old_dist = self.matrix[names[0]][names[1]]

			first_dist = (old_dist+(first_sum-second_sum)/(len(self.matrix)-2))*0.5
			second_dist = (old_dist+(second_sum-first_sum)/(len(self.matrix)-2))*0.5

			# print first_dist, second_dist

			newNode = TwoChildNode (names[0], names[1], first_dist, second_dist)

			self._rebuild_with (newNode, names[0], names[1])

	def _find_closest (self) :
		min_distance = 10000000000000000
		min_dude1 = None
		min_dude2 = None
		for dude1, dude1_matrix in self.matrix.items():
			for dude2 in dude1_matrix:
				if dude2 == dude1:
					continue
				distance = self.matrix[dude1][dude2]*(len(self.matrix)-2)-sum(self.matrix[dude1].values())-sum(self.matrix[dude2].values())
				print dude1, dude2, distance
				if distance < min_distance :
					min_dude1 = dude1
					min_dude2 = dude2
					min_distance = distance
					# print self.matrix[dude1][dude2]*(len(self.matrix)-2), sum(self.matrix[dude1].values()), sum(self.matrix[dude2].values())
		print 'dudes:', min_dude1, min_dude2
		return min_dude1, min_dude2

	def _rebuild_with(self, new_node, old_node1, old_node2) :
		new_matrix = defaultdict(dict)

		old_dist = self.matrix[old_node1][old_node2]
		
		for node in self.matrix :
			if id(node) != id(old_node1) and id(node) != id(old_node2) :

				for node2 in self.matrix[node]:
					if id(node2) != id(old_node1) and id(node2) != id(old_node2) : 
						new_matrix[node][node2] = self.matrix[node][node2]

				val = (self.matrix[old_node1][node]+self.matrix[old_node2][node]-old_dist)*0.5
				new_matrix[new_node][node] = val
				new_matrix[node][new_node] = val

		self.matrix = new_matrix
		# print len(self.matrix)

def calculate_distance (first, second) :
	distance = 0
	for i in range (len(first)) :
		if first[i] != second[i] :
			distance += 1
	# print distance
	return distance