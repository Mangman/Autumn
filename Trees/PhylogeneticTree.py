#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse

from NJMatrix import NJMatrix 
from Utilities import parse_nex
from Node import SingleChildNode

import sys

parser = argparse.ArgumentParser(description="Creates phylogenic tree.")
parser.add_argument('-r', '--reads', type=str, help="Nex file with species\' reads")


#  Парсинг fastq
args = parser.parse_args()

reads = parse_nex(args.reads)
matrix = NJMatrix(reads)

# a = SingleChildNode("a")
# b = SingleChildNode("b")
# c = SingleChildNode("c")
# d = SingleChildNode("d")
# e = SingleChildNode("e")

# #                     a   b   c   d   e
# matrix.matrix = {a: {a:0,b:5,c:9,d:9,e:8}, 
# 			     b: {a:5,b:0,c:10,d:10,e:9},
# 			     c: {a:9,b:10,c:0,d:8,e:7},
# 			     d: {a:9,b:10,c:8,d:0,e:3},
# 			     e: {a:8,b:9,c:7,d:3,e:0}}
matrix.join_neighbours()

#  Распечатка
with open('Tree.output', 'w') as output :
	old_stdout = sys.stdout
	sys.stdout = output

	vertexes = matrix.matrix.keys()

	first = vertexes[0]
	second = vertexes[1]
	third = vertexes[2]

	print "({}:0.5, {}:0.43, {}:0.35);".format(first, second, third)
	sys.stdout = old_stdout