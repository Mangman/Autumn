#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from itertools import islice

def reverseComplimentary(s) :
	complimentary = {'A': 'T',
				     'T': 'A',
				     'G': 'C',
				     'C': 'G'}

	def transform (ch) :
		if ch in complimentary :
			return complimentary[ch]
		else :
			return ch

	result = "".join(map(transform, s[::-1]))
	return result

def loadFastq (filePath) :
	reads = []
	with open(filePath) as f :
		for line in islice(f, 1, None, 4) :
			reads.append(line.strip())
	return reads