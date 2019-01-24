#creates the paper venue and its name mappings
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

def extract_id(line):
	start = '['
	end = ']'
	s = line
	return s[s.find(start)+len(start):s.rfind(end)]

def remove_bracket(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret


# DATA_PATH = "/ssd-scratch/ayush/Text"
DATA_PATH = "./Text"

datasets = listdir(DATA_PATH)

c = 0

PAPER_VENUE_NAME_DICT = {}
num_index_papers = 0
for dataset in datasets:
	print(dataset)
	if dataset.split("_")[-1] != 'data.txt':
		continue
	dataset_path = DATA_PATH + "/" + dataset
	f = open(dataset_path, 'r' , encoding = 'utf-8')
	line = f.readline()
	line = (line.encode('ascii', 'ignore')).decode("utf-8")
	while line:
		if line[:6] == '#index':
			num_index_papers += 1
		if (line[:2] == "#j" or line[:2] == "#c"):
			venue_id = extract_id(line)
			PAPER_VENUE_NAME_DICT[venue_id] = remove_bracket(line[2:-1]) 
		line = f.readline()
		line = (line.encode('ascii', 'ignore')).decode("utf-8")
		c += 1
		if c % 10**5 == 0:
			print(c)
	print("{} DONE".format(dataset))
	c = 0



