#!/usr/bin/python
# -*- coding: utf-8 -*-

from Alignment import AlignmentMatrix, merge
from StepanBioUtilities import reverseComplimentary, matrixPrint

import sys
import argparse

class GenesMismatchTable :
	table = {} 
	entries = {}

	def __init__ (self, genesFile) :
		# #  Костыльный метод
		# currentGene = ""
		# for line in genesFile :		
		# 	if line[0] == '>' :
		# 		if currentGene != "":
		# 			self.entries[currentGene] = 0
		# 			self.table[currentGene] = [0]*len(currentGene)
		# 		currentGene = ""
		# 		continue
		# 	else :
		# 		currentGene += line.strip()
		for line in genesFile :
			if line[0] == ">" :
				continue
			else :
				currentGene = line.strip()
				self.entries[currentGene] = 0
				self.table[currentGene] = [0]*len(currentGene)
		

	def appendMismatches (self, gene, alignedGene, alignedRead) :
		originalGenePos = -1
		for i in range (0, len(alignedGene)) :
			first = alignedGene[i]
			second = alignedRead[i]
			if first == '-':
				originalGenePos -= 1
			if first != '-' and second != '-' :
				if first != second :
					self.table[gene][originalGenePos] += 1
					self.entries[gene] += 0
			originalGenePos += 1

parser = argparse.ArgumentParser(description='Count mismathches on gene alignment.')
parser.add_argument('-r', '--reads', type=str, help='fasta file with reads for alignment')
parser.add_argument('-g', '--genes', type=str, help='genes base')

args = parser.parse_args()

with open(args.reads) as reads, open(args.genes) as genes:
	
	mismatchTable = GenesMismatchTable(genes)

	i = 0
	for read in reads :
		
		if read[0] == '>' :
			continue
		else : 
			#TODO: пихнуть в функцию
			bestScore = 0
			bestMatrix = AlignmentMatrix (False, '', '')
			bestGene = ""
			for gene in mismatchTable.table.keys() :
				currenMatrix = AlignmentMatrix(False, gene, read)
				print currenMatrix.largestScore
				print ""
				print gene
				print ""
				print read
				if currenMatrix.largestScore[0] > bestMatrix.largestScore[0] :
					bestMatrix = currenMatrix
					bestGene = gene
			print ""

			res = bestMatrix.alignReads()
			#  Забил на память. Лучше пофиксить
			mismatchTable.appendMismatches(bestGene, res[0], res[1])
			i += 1
			if i == 50: break 
	print mismatchTable.table
				