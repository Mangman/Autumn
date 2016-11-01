#!/usr/bin/python
# -*- coding: utf-8 -*-

class BruijnGraph :
	edges = []	 # {name1: {name2: [part, count] } }
	names = {}
	k = None


	#  КОМПЛИМЕНТАРНОСТЬ КОМПЛИМЕНТАРНОСТЬ
	def __init__(self, reads, partLen) :
		self.k = partLen+1

		#  Не хочу два раза проходить ;(
		self._fillEdgedWithSadLonelyEmptiness(reads)
		self._fillEdgesWithRealShit(reads)

	def _fillEdgedWithSadLonelyEmptiness(self, reads) :
		numberOfReads = 0
		for read in reads:
			#  Проход рамкой размером с вершину графа
			currentPart = read[0:self.k-1]

			for ch in read[self.k-1:] :
				#  Инициализация словаря
				if currentPart not in self.names :
					self.names[currentPart] = numberOfReads
					numberOfReads += 1
					self.edges.append (dict())
				#  Присоединяем следующий нуклеотид и удаляем первый для сдвига рамки
				currentPart = currentPart[1:]
				currentPart += ch


	def _fillEdgesWithRealShit (self, reads) :
		for read in reads :
			#  Обозначения ребра графа
			currentPart = read[0:self.k]
			
			for ch in read[self.k:] :
				#  Обозначение вершин грава
				firstChunk = self.names[currentPart[0:self.k-1]]
				secondChunk = self.names[currentPart[1:]]
				#  Инициализация при первом обращении (Медленно, возможно)
				if secondChunk not in self.edges[firstChunk] :
					self.edges[firstChunk][secondChunk] = [currentPart, 0]
				#  Увеличение количества встреч наложения
				self.edges[firstChunk][secondChunk][1] += 1
				#  Присоединяем следующий нуклеотид и удаляем первый для сдвига рамки
				currentPart = currentPart[1:]
				currentPart += ch
