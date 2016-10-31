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
				#  Зануление отрицательных скоров для локального выравнивания
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

		#  Выравнивание по пути из матрицы пути
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
			#  Сложные расчеты (выравнивание кусков слева и справа для последующего мерджа)
			elif path == 0 :
				rightAddition = self.s2[self.largestScore[1]:]
				leftAddition = self.s1[0:j]
				aligned1 = leftAddition+aligned1[::-1]+("-"*len(rightAddition))
				aligned2 = "-"*len(leftAddition)+aligned2[::-1]+rightAddition
				break
		
		#  При локальном выравнивании части уже развернуты
		if self.isGlobal :
			aligned1 = aligned1[::-1]
			aligned2 = aligned2[::-1]
		return (aligned1, aligned2)

def merge (first, second, quality1, quality2) :
	result = ""

	q1 = 0
	q2 = 0
	for i in range (len(first)) :
		a = first[i]
		b = second[i]

		appendingChar = ''
		if a == b : appendingChar = a
		elif a == '-' : 
			appendingChar = b
			q1 -= 1
		elif b == '-' : 
			appendingChar = a
			q2 -= 1
		elif a != b : 
			if ord(quality1[q1]) > ord(quality2[q2]) :
				appendingChar = a
			else :
				appendingChar = b 
		result += appendingChar

		q1 += 1
		q2 += 1
	return result