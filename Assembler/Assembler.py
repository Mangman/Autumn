#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
import time

from Utilities import reverseComplimentary, loadFastq
from BruijnGraph import BruijnGraph


parser = argparse.ArgumentParser(description='Assembles reads to genome.')
parser.add_argument('-r', '--reads', type=str, help='Fasta file with reads for assempling')
parser.add_argument('-k', type=int, help = 'Length of parts, we set as verticies')

#  Парсинг fastq
args = parser.parse_args()
reads = loadFastq(args.reads)

tic = time.clock()
#  Инициализация графа
a = BruijnGraph(reads, args.k)

#  Распечатка
with open('Graph.output', 'w') as output :
	oldStdout = sys.stdout
	sys.stdout = output
	print a.edges
	sys.stdout = oldStdout

a.generateGraph()

toc = time.clock()
print ">Process ended.\n>Time spent-- "+str(toc - tic)

print len(a.edges.keys())