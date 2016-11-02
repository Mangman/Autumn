#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from itertools import islice

def reverse_complimentary(s) :
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

def load_fastq (file_path) :
	reads = []
	with open(file_path) as f :
		for line in islice(f, 1, None, 4) :
			reads.append(line.strip())
	return reads