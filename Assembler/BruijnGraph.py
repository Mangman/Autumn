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
				print "heh"
				if len(self.edges[current]) == 1 :
					succeding = list(self.edges[current])[0]
					if len(self.incoming[succeding]) == 1 :
						
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
						del self.edges[current]
				else :
					print "outta sequence"
			if join_counter > old_join_counter :
				old_join_counter = join_counter
				print "next"
			else :
				print "end"
			break

	# def condensate (self, condensated) :
	# 	print "lal"
	# 	# for next_part in self.edges[start_part].keys():
	# 	# 	if len(self.edges[next_part].keys()) > 1 :
	# 	# 		self.condensate(next_part, graph)
	# 	# 	elif len(self.edges[next_part].keys()) == 1 :
	# 	# 		next_next_part = self.edges[next_part].keys()[0]

	# 	# 		first_connection = self.edges[start_part][next_part]
	# 	# 		second_connection = self.edges[next_part][next_next_part]
	# 	# 		first_connection_len = len(first_connection)
	# 	# 		second_connection_len = len(second_connection)

	# 	# 		average_coverage = (first_connection[1]*first_connection_len+second_connection[1]*second_connection_len)\
	# 	# 							/(second_connection_len+first_connection_len)
	# 	# 		graph[start_part][next_next_part] = [first_connection[0]+second_connection[0][-1], average_coverage]
	# 	# 		self.condensate(next_part, graph)
	# 	names = set(self.edges.keys()) 


	# 	for name in names:
	# 		if name not in condensated and len(self.edges[name]) == 1 and self.incoming[name][1] == 1 : # or self.incoming[name][1] == 0) :
	# 			previous = self.incoming[name][0]
	# 			succeding = self.edges[name].keys()[0]
	# 			#print previous, name
	# 			#print self.edges[previous]
	# 			first_connection = self.edges[previous][name]
	# 			second_connection = self.edges[name][succeding]

	# 			#Пофиксить
	# 			condensated[previous][succeding] = [first_connection[0]+second_connection[0][-1], (first_connection[1]+second_connection[1])/2] 
	# 			#print (succeding, previous, first_connection[0]+second_connection[0][-1])
	# 			self._lal(previous, succeding, condensated)
	# 			print 'hah'
	# 		else :
	# 			condensated[name] = deepcopy(self.edges[name])

	# def _lal (self, previous, current, condensated) :
	# 	if current not in condensated and len(self.edges[current]) == 1 and self.incoming[current][1] == 1 :
	# 		succeding = deepcopy(self.edges[current].keys()[0])
	# 		#print condensated[previous]
	# 		first_connection = condensated[previous][current]
	# 		second_connection = deepcopy(self.edges[current][succeding])

	# 		#Пофиксить
	# 		del condensated[previous][current]
	# 		#print condensated[previous]
	# 		condensated[previous][succeding] = [first_connection[0]+second_connection[0][-1], (first_connection[1]+second_connection[1])/2] 
	# 		self._lal(previous, succeding, condensated)
	# 	# elif current not in condensated and len(self.edges[current]) > 1 and self.incoming[current][1] == 1 :
	# 	# 	first_connection = condensated[previous][current]
	# 	# 	second_connection = self.edges[current][succeding]

	# 	# 	#Пофиксить
	# 	# 	del condensated[previous][current]
	# 	# 	condensated[previous][succeding] = [first_connection[0]+second_connection[0][-1], (first_connection[1]+second_connection[1])/2] 
	# 	# 	self._lal(previous, succeding, condensated)
	# 	else :
	# 		condensated[current] = deepcopy(self.edges[current])
	# 		for name in self.edges[current] :
	# 			#print self.edges[current]
	# 			#print name
	# 			#print '\n'
	# 			self._lal(current, name, condensated)


