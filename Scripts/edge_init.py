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





DATA_PATH = "/ssd-scratch/ayush/Text"
datasets = listdir(DATA_PATH)

G = nx.DiGraph()
c = 0
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
		if line[:6] == '#index':
			name = line[6:-1]
		elif line[:3] == '#%*' and name != "":
			line_array = line.split("[")
			paper_cited_by_index_name = line_array[-1][:-2]
			G.add_edge(name , paper_cited_by_index_name)
		elif line[:3] == "#$*" and name != "":
			line_array = line.split("[")
			paper_citing_index_name = line_array[-1][:-2]
			G.add_edge(paper_citing_index_name , name)
		line = f.readline()
		line = (line.encode('ascii', 'ignore')).decode("utf-8")

		c += 1
		if c % 10**5 == 0:
			print(c)
	print("{} DONE".format(dataset))
	c = 0

print(G.edges())
dump_file('G' , G)