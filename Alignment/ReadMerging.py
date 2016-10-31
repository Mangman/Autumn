#!/usr/bin/python
# -*- coding: utf-8 -*-

from Alignment import AlignmentMatrix, merge
from StepanBioUtilities import reverseComplimentary, matrixPrint

import sys

with open("1.fq") as f1, open("2.fq") as f2, open("output.fasta", "w") as output:
	i = 0
	quality1 = ""
	quality2 = ""

	res = None

	for line1 in f1:
		for line2 in f2:
			if i%4 == 1 :
				if i%40 == 1 :
					print i			
				reversedLine2 = reverseComplimentary(line2)
				a = AlignmentMatrix(False, next(f1), reversedLine2)
				res = a.alignReads()
			if i%4 == 3 :
				next(f1)
				quality1 = next(f1)
				next(f1)
				quality2 = line2
				merged = merge(res[0], res[1], quality1, quality2)
				output.write("\n>lal\n"+merged)
			i += 1
		print "ended"
		sys.exit()
