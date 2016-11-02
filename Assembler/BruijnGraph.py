#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict

from Utilities import reverseComplimentary 

class BruijnGraph :
	edges = defaultdict(dict)# {name1: {name2: [part, count] } }
	k = None

	def __init__(self, reads, partLen) :
		self.k = partLen+1

		self._fillEdges(reads)


	def _fillEdges(self, reads) :
		for read in reads :
			#  Обозначения ребра графа

			for i in range(self.k, len(read)+1):
				currentPart = read[i-self.k : i]
				self._setEdge(currentPart)
				self._setEdge(reverseComplimentary(currentPart))

	def _setEdge (self, part) :
		#  Обозначение вершин грава
		firstChunk = part[:-1]
		secondChunk = part[1:]
		#  Инициализация при первом обращении (Медленно, возможно)
		if secondChunk not in self.edges[firstChunk] :
			self.edges[firstChunk][secondChunk] = [part, 0]
		#  Увеличение количества встреч наложения
		self.edges[firstChunk][secondChunk][1] += 1

	def generateGraph (self) :
		with open('Graph.dot', 'w') as output :
			oldStdout = sys.stdout 
			sys.stdout = output
			for name1, val in self.edges.items() :
				for name2, arr in val.items() :
					print "{} -> {} [label = \"{}\"];".format(name1, name2, arr[1])
			sys.stdout = oldStdout

