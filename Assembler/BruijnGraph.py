#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
from copy import deepcopy

from Utilities import reverse_complimentary 

class BruijnGraph :
	edges = defaultdict(dict)# {name1: {name2: [part, count] } }
	incoming = defaultdict(set)
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

		self.incoming[second_chunk].add(first_chunk)

	def condensate (self) :
		
		old_join_counter = 0
		join_counter = old_join_counter

		while (True) :
			names = deepcopy(self.edges.keys())
			for current in names :
				if len(self.edges[current]) == 1 :#and len(self.incoming[current]) == 1 :
					succeding = list(self.edges[current])[0]
					if len(self.incoming[succeding]) == 1 : #and len(self.edges[succeding]) == 1 :
						
						current_link = self.edges[current][succeding]
						for incoming in self.incoming[current] :
							incoming_link = self.edges[incoming][current]
							new_link = [incoming_link[0]+current_link[0][-1], (incoming_link[1]+current_link[1])/2]

							del self.edges[incoming][current]
							self.edges[incoming][succeding] = new_link
							self.incoming[succeding].add(incoming)
							join_counter += 1 
							#print 'compressed'

						self.incoming[succeding].remove(current)
						del self.incoming[current]
						del self.edges[current]
			if join_counter > old_join_counter :
				old_join_counter = join_counter

			#  Только один проход -- можно пофиксить
			break

	#  TODO: выбор из двух тупиков
	def cut_excessive (self, DEAD_END_THRESHOLD, CAP_THRESHOLD) :
		names = set(deepcopy(self.edges.keys()))
		new_names = deepcopy(names)
		#  Находим тупики не особо оптимально
		for name in names :
			temp = self.edges[name]
			for read in temp :
				new_names.add(read)
		names = new_names

		for current in names :
			# Надстройка - "шапка", но с ней все мутно 
			if len(self.incoming[current]) == 0 and len(self.edges[current]) == 1 :
				succeding = self.edges[current].keys()[0]
				link = self.edges[current][succeding]

				if link[1] < CAP_THRESHOLD :
					del self.edges[current]
					self.incoming[succeding].remove(current)
			#  тупик
			elif len(self.incoming[current]) == 1 and len(self.edges[current]) == 0 :
				previous = list(self.incoming[current])[0]
				link = self.edges[previous][current]

				if link[1] < DEAD_END_THRESHOLD :
					del self.edges[current]
					del self.incoming[current]
					del self.edges[previous][current]
