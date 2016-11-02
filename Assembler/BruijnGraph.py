#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict

from Utilities import reverse_complimentary 

class BruijnGraph :
	edges = defaultdict(dict)# {name1: {name2: [part, count] } }
	k = None

	def __init__(self, reads, part_len) :
		self.k = part_len+1

		self._fill_edges(reads)


	def _fill_edges(self, reads) :
		for read in reads :
			for i in range(self.k, len(read)+1):
				current_part = read[i-self.k : i]
				self._set_edge(current_part)
				self._set_edge(reverse_complimentary(current_part))

	def _set_edge (self, part) :
		#  Обозначение вершин грава
		first_chunk = part[:-1]
		second_chunk = part[1:]
		#  Инициализация при первом обращении (Медленно, возможно)
		if second_chunk not in self.edges[first_chunk] :
			self.edges[first_chunk][second_chunk] = [part, 0]
		#  Увеличение количества встреч наложения
		self.edges[first_chunk][second_chunk][1] += 1

	def generate_graph (self) :
		with open('Graph.dot', 'w') as output :
			old_stdout = sys.stdout 
			sys.stdout = output
			for name1, val in self.edges.items() :
				for name2, arr in val.items() :
					print "{} -> {} [label = \"{}\"];".format(name1, name2, arr[1])
			sys.stdout = old_stdout

