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

def generate_dot_graph (edges, file_path) :
	with open(file_path, 'w') as output :
		old_stdout = sys.stdout 
		sys.stdout = output
		print "digraph G {"
		for name1, val in edges.items() :
			for name2, arr in val.items() :
				print "{}[label=\"\"]{}[label=\"\"]".format(name1, name2)
				print "\t{} -> {}[label={}];".format(name1, name2, arr[1], arr[0])
				#print "\t{} -> {} [label = \"{}\n{}\"];".format(name1, name2, arr[1], arr[0])
		print "}"
		sys.stdout = old_stdout



