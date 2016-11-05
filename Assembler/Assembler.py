#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
import time

from collections import defaultdict

from Utilities import reverse_complimentary, load_fastq, generate_dot_graph
from BruijnGraph import BruijnGraph


parser = argparse.ArgumentParser(description='Assembles reads to genome.')
parser.add_argument('-r', '--reads',               type=str, help='Fasta file with reads for assembling')
parser.add_argument('-k',                          type=int, help = 'Length of parts, we set as verticies')
parser.add_argument('-dt', '--dead_end_threshold', type=int, default = 0, help = 'Dead end coverage threshold.')
parser.add_argument('-ct', '--cap_threhold',       type=int, default = 0, help = '\'Cap\' coverage threshold')

#  Парсинг fastq
args = parser.parse_args()
reads = load_fastq(args.reads)

tic = time.clock()
#  Инициализация графа
a = BruijnGraph(reads, args.k)

#  Распечатка
with open('Graph.output', 'w') as output :
	old_stdout = sys.stdout
	sys.stdout = output
	sys.stdout = old_stdout

a.condensate()
a.cut_excessive(args.dead_end_threshold, args.cap_threhold)
a.condensate()
generate_dot_graph(a.edges, 'conprsd.dot')

toc = time.clock()
print ">Process ended.\n>Time spent-- "+str(toc - tic)

print len(a.edges.keys())
