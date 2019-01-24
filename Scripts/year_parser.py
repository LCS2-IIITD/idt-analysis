import networkx as nx 
import pickle
import random 
import collections
import operator
import sys
import re 
from os import listdir
from os.path import isfile, join
import os 

def get_pickle_dump(filename):
	with open('./dumps/'+filename+'.pickle','rb') as handle:
		Variable = pickle.load(handle)
	return Variable

def dump_file(filename, Variable):
	with open('./dumps/'+filename+'.pickle','wb') as handle:
		pickle.dump(Variable,handle,protocol=pickle.HIGHEST_PROTOCOL)


def all_edges_in_set_A(P,n, done):
	print("Called by {}".format(n))
	e_list = list(P.out_edges(nbunch = n))
	# print(e_list)
	for e in e_list:
		if e[1] not in done:
			return False
	return True


DATA_PATH = "/ssd-scratch/ayush/Text"

datasets = listdir(DATA_PATH)

c = 0

PAPER_YEAR_DICT = {}
# PAPER_NAME = {}
for dataset in datasets:
	print(dataset)
	if dataset.split("_")[-1] != 'data.txt':
		continue
	dataset_path = DATA_PATH + "/" + dataset
	f = open(dataset_path, 'r')
	line = f.readline()
	line = (line.encode('ascii', 'ignore')).decode("utf-8")
	name = ""
	while line:
		if line[:6] == "#index":
			name = line[6:-1]
		elif line[:2] == "#y" and name != "" and line[:4] != "#ypp" and line[:5] != "#yno.":
			year = line[2:-1]
			# print(line)
			PAPER_YEAR_DICT[name] = year 
			name = ""
		elif line[:3] == '#%*':
			line_array = line.split("[")
			name = line_array[-1][:-2]

		elif line[:3] == '#%y' and name != "" and line[:5] != "#%ypp" and line[:6] != "#%yno.":
			year = line[3:-1]
			# print(line)
			PAPER_YEAR_DICT[name] = year
			name = ""
		elif line[:3] == '#$*':
			line_array = line.split("[")
			name = line_array[-1][:-2]

		elif line[:3] == '#$y' and name != "" and line[:5] != "#$ypp" and line[:6] != "#$yno.":
			year = line[3:-1]
			# print(line)
			PAPER_YEAR_DICT[name] = year
			name = ""
		line = f.readline()
		line = (line.encode('ascii', 'ignore')).decode("utf-8")

		c += 1
		if c % 10**5 == 0:
			print(c)
	print("{} DONE".format(dataset))
	c = 0


dump_file('PAPER_YEAR_DICT', PAPER_YEAR_DICT)

