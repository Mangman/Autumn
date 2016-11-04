#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def parse_nex (filePath) :
	
	reads = {}

	with open (filePath) as file:
		for line in file :
			read = line.strip().split()
			reads[read[0]] = read[1]


	return reads