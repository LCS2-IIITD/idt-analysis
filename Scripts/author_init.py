import networkx as nx 
import pickle
import random 
import collections
import operator
from sys import exit 
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


def get_paper_id(line):
	paper_name = False
	paper_main_name = ""
	for s in line:
		if s == '[':
			paper_name = True 
		if paper_name:
			paper_main_name += s 
		if s == ']':
			paper_main_name = "" 
			paper_name = False
			break 
	return paper_main_name 


def get_all_authors(line):
	authors = set() 
	author_name = False
	author_main_name = ""
	for s in line:
		if s == '[':
			author_name = True 
		if author_name:
			author_main_name += s 
		if s == ']':
			authors.add(author_main_name) 
			author_main_name = "" 
			author_name = False 

	return authors



DATA_PATH = "Text"
datasets = listdir(DATA_PATH)

G = nx.DiGraph()
c = 0
total_authors = 0
papers = 0
authors_dict = {} 
cur_visited_papers = set()
for dataset in datasets:
	print(dataset)
	if dataset.split("_")[-1] != 'data.txt':
		continue
	dataset_path = DATA_PATH + "/" + dataset
	f = open(dataset_path, 'rb')
	line = f.readline()
	line = line.decode('utf-8')
	name = ""
	cur_paper = ""
	while line:
		if line[:6] == '#index':
			# print('FOUND NEW INDEX PAPER') 
			cur_paper = line[6:-1] 
			line = f.readline() 
			line = f.readline()
			line = line.decode('utf-8') 

			authors = get_all_authors(line) 
			for v in authors:
				if v not in authors_dict:
					authors_dict[v] = 1
				else:
					authors_dict[v] += 1
		line = f.readline()
		line = line.decode('utf-8')

		c += 1
		if c % 10**5 == 0:
			print(c)
	print("{} DONE".format(dataset))
	c = 0

x = 0 
for v in authors_dict:
	x += authors_dict[v] 

print(x / len(authors_dict))

dump_file('authors_dict' , authors_dict) 
