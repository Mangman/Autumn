#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def reverseComplimetary(s) :
	complimentary = {'A': 'T',
				     'T': 'A',
				     'G': 'C',
				     'C': 'G'}

	def transform (ch) :
		if ch in complimentary :
			return complimentary[ch]
		else :
			return ch

	return map(transform, s[::-1])

def matrixPrint (matrix, s1, s2) :
		#Пишем буквы на горизонтальной оси
		print "Matrix:"
		topStr = "     - "
		for ch in s1 :
			topStr+=("  "+str(ch)+" ")
		print topStr
		
		#Выравниваем числа и печатаем вместе с буквами на вертикальной оси
		newS2 = "-"+s2
		i = 0
		formatedMatrix = []
		for arr in matrix :
			
			formatedMatrix.append(list())
			
			for val in arr :
				spacing = ""
				if val > 10 or (val < 0 and val > -10) :
					spacing = "  "
				elif val >= 0 and val < 10 :
					spacing = "   "
				formatedMatrix[-1].append(spacing+str(val))
			
			sys.stdout.write(newS2[i]+'|')
			
			for num in formatedMatrix[-1] :
				sys.stdout.write(num)
			
			print ' |'
			i+= 1