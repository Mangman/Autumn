#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from StepanBioUtilities import matrixPrint

#TODO:  Наследование?
class AlignmentMatrix :
	matrix = []
	largestScore = (0, -1,-1)  #   Значение и координаты наибольшего скора для локального выравнивания
	trace  = []


	isGlobal = 1

	s1 = ""
	s2 = ""

	len1 = -1
	len2 = -1

	def __init__(self, isGlobal , s1, s2) :
		self.s1 = s1
		self.s2 = s2 

		self.len1 = len(self.s1)
		self.len2 = len(self.s2)

		self.isGlobal = isGlobal

		#  Заполняем матрицы экзистенциальной пустотой
		for i in range (self.len2+1) :
			self.matrix.append(list())
			self.trace.append(list())
		
		#  Трейс нулями, чтобы не аппендить потом
		for i in range (self.len2+1) :
			for j in range (self.len1+1):
				self.trace[i].append(0)

		#  Верхняя строка трейса заполняется единицами для возвращения в начальную точку
		self.trace[0] = [0]+[1]*(self.len1)
		
		#  Первоначальные значения матриц
		if self.isGlobal : self._initGlobal()
		else : self._initLocal()
		
		self._fillMatrix()

	def _initGlobal (self) :
		for i, value in zip(range(1, self.len2+1), range(-self.len2, 0)[::-1]) :
			self.matrix[i].append(value)
			self.trace[i][0] = 3
		self.matrix[0] = range(-self.len1, 0+1)[::-1]

	def _initLocal (self) :
		for i in range(1, self.len2+1) :
			self.matrix[i].append(0)
			self.trace[i][0] = 3
		self.matrix[0] = [0]*(self.len1+1)
	

	def _fillMatrix(self) :
		for i in range (1, self.len2+1) :
			for j in range (1, self.len1+1) :
				
				left = self.matrix[i][j-1]
				upper = self.matrix[i-1][j]
				leftUpper = self.matrix[i-1][j-1]

				#  Выбор наибольшего значения из предыдущих для оптимального пути
				maximum = max([left, upper, leftUpper])
				delta = 0

				#  Штраф за мисматч и индел -1, за совпадение +1
				if leftUpper == maximum :
					if self.s1[j-1] == self.s2[i-1] :
						delta = +1
					else :
						delta = -1
					self.trace[i][j] = 2
				elif left == maximum :
					delta = -1
					self.trace[i][j] = 1
				elif upper == maximum :
					delta = -1
					self.trace[i][j] = 3

				score = maximum+delta
				if self.isGlobal != 1 :
					if score < 0 : 
						score = 0
						self.trace[i][j] = 0
				if score > self.largestScore[0] :	
					self.largestScore = (score, i, j)

				self.matrix[i].append(score)

	#TODO:  Нормально сделать
	def alignReads(self):
		i = self.largestScore[1]
		j = self.largestScore[2]

		aligned1 = ""
		aligned2 = ""

		merged = ""

		while (i != 0 and j != 0) :
			path = self.trace[i][j]
			if path == 2 :
				aligned2 += self.s2[i-1]
				aligned1 += self.s1[j-1]
				i = i-1
				j = j-1 
			elif path == 1 :
				aligned2 += '-'
				aligned1 += self.s1[j-1]
				j = j-1
			elif path == 3 :
				aligned1 += '-'
				aligned2 += self.s2[i-1]
				i = i-1
			elif path == 0 :
				merged = s1[0:j]+aligned1[::-1]+s2[self.largestScore[2]:]
				break
		print "here come dat boi"
		print "aww shit waddup"
		return (aligned1[::-1], aligned2[::-1])

def merge (first, second) :
	result = ""
	for i in range (len(first)) :
		a = first[i]
		b = second[i]

		appendingChar = ''
		if a == b : appendingChar = a
		elif a == '-' : appendingChar = b
		elif b == '-' : appendingChar = a
		elif a != b : appendingChar = 'N'#  TODO: хз что делать ;( 
		result += appendingChar
	return result


s1 = "ACCCAAAAACCACACCCCTCCTTGGGAGAATCCCCTAGATCACAGCTCCTCACCATGGACTGGACCTGGAGCATCCTTTTCTTGGTGGCAGCAGCAACAGGTGCCCACTCCCAGGTTCAGCTGGTGCAGTCTGGAGCTGAGGTGAAGAAGCCTGGGGCCTCAGTGAAGGTCTCCTGCAAGGCTTCTGGTTACACCTTTACCAGCTATGGTATCAGCTGGGTGCGACAGGCCCCTGGACAAGGGCTTGAGTGGATGGGATGGATCAGCGCTTACAATGGTAACACAAACTATGCACAGAAG"
s2 = "AGAGGAAGTCCTGTGCGAGGCAGCCAACGGCCACGCTGCTCGTATCCGACGGGGAATTCTCACAGGAGACGAGGGGGAAAAGGGTTGGGGCGGATGCACTCCCTGAGGAGACGGTGACCAGGGTTCCCTGGCCCCAGTAGTCGGCGGGCTCCCCGCCGACACAGTAATCCACGGCCGTGTCGTCAGATCTCAGGCTCCTCAGCTCCATGTAGGCTGTGCCCGTGGATGTGTCTGTGGTCATGGTGACTCTGCCCTGGACCTTCTGTGCCTAGTTTGTGTTACCATTGTAAGCGCTGACCC"
a = AlignmentMatrix(0, s1, s2)
#matrixPrint(a.matrix, a.s1, a.s2)
res = a.alignReads()
print merge(res[0], res[1])