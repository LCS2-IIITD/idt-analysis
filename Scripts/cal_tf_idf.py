#this script calculates the TF-IDF factor of the paper 
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
import pandas as pd 
from math import log10

def get_pickle_dump(filename):
  with open('./dumps/'+filename+'.pickle','rb') as handle:
    Variable = pickle.load(handle)
  return Variable

def dump_file(filename, Variable):
  with open('./dumps/'+filename+'.pickle','wb') as handle:
    pickle.dump(Variable,handle,protocol=pickle.HIGHEST_PROTOCOL)


G = get_pickle_dump('G_without_cycles') 
 
def graph_traversal(H , cur_paper , shortest_path , cur_distance):
  inbound_edges = list(H.in_edges(nbunch = cur_paper))
  if(len(inbound_edges) == 0):
    if cur_paper in shortest_path:
      if cur_distance < shortest_path[cur_paper]:
        shortest_path[cur_paper] = cur_distance
    else:
      shortest_path[cur_paper] = cur_distance 
    # print(cur_paper)
    return 
  for e in inbound_edges:
    graph_traversal(H , e[0] , shortest_path , cur_distance + 1) 


def calculate_tfidf(H , cur_paper, shortest_path , cur_distance, idf):
  global tfidf
  inbound_edges = list(H.in_edges(nbunch = cur_paper))
  if(len(inbound_edges) == 0):
    if shortest_path[cur_paper] == cur_distance:
      tfidf += cur_distance * log10(1 + (1 / (idf + 2)))
      # print(tfidf)
    return 

  idf += len(inbound_edges) - 1 
  for e in inbound_edges:
    calculate_tfidf(H , e[0] , shortest_path , cur_distance + 1 , idf)  

GLOBAL_TF_IDF = {}
for paper in G.nodes().copy(): 

  induced_graph = set()
  induced_graph_list = list(G.in_edges(nbunch = paper))
  for e in induced_graph_list:
    induced_graph.add(e[0])

  induced_graph.add(paper)
  H = G.subgraph(induced_graph)
  # print(H.edges())
  shortest_path = {} 
  for e in H.nodes():
    e_list = list(H.out_edges(nbunch = e))
    if len(e_list) > 1:
      H.remove_edge(e , paper) 
  num_calls = 0
  print("******************************{}*************************************".format(paper))
  print(len(H.edges()))
  graph_traversal(H , paper , shortest_path , 0) 
  # print(shortest_path) 
  tfidf = 0
  calculate_tfidf(H , paper , shortest_path, 0 , 0) 
  print("TF IDF for paper {} is {}".format(paper , tfidf))
  GLOBAL_TF_IDF[paper] = tfidf 
  tfidf = 0


dump_file('GLOBAL_TF_IDF' , GLOBAL_TF_IDF)