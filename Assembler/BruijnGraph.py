#!/usr/bin/python
# -*- coding: utf-8 -*-

class BruijnGraph :
	edges = {}	 # {name1: {name2: [part, count] } }
	k = None

	def __init__(self, reads, partLen) :
		self.k = partLen+1

		#  Не хочу два раза проходить ;(
		self._fillEdgedWithSadLonelyEmptiness(reads)
		self._fillEdgesWithRealShit(reads)



	def _fillEdgedWithSadLonelyEmptiness(self, reads) :
		for read in reads:
			currentPart = read[0:self.k]
			for ch in read[self.k:] :
				firstChunk = currentPart[0:self.k-1]
				secondChunk = currentPart[1:]
				#  Говнокод
				if firstChunk not in self.edges :
					self.edges[firstChunk] = {}
				if secondChunk not in self.edges :
					self.edges[secondChunk] = {}
				currentPart = currentPart[1:]
				currentPart += ch

	def _fillEdgesWithRealShit (self, reads) :
		for read in reads :
			currentPart = read[0:self.k]
			for ch in read[self.k:] :
				firstChunk = currentPart[0:self.k-1]
				secondChunk = currentPart[1:]
				if secondChunk not in self.edges[firstChunk] :
					self.edges[firstChunk][secondChunk] = [currentPart, 0]
				self.edges[firstChunk][secondChunk][1] += 1

				currentPart = currentPart[1:]
				currentPart += ch
