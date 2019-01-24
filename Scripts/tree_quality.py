#this script calculates the branch niceness 
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
        return 
    for e in inbound_edges:
        graph_traversal(H , e[0] , shortest_path , cur_distance + 1) 


def calculate_branch_niceness(H , cur_paper, shortest_path , cur_distance, branch_niceness):
    global all_branch_niceness 
    inbound_edges = list(H.in_edges(nbunch = cur_paper))
    outbound_edges = list(H.out_edges(nbunch = cur_paper))
    branch_niceness += (inbound_edges + outbound_edges)
    if(len(inbound_edges) == 0):
        if shortest_path[cur_paper] == cur_distance:
            all_branch_niceness.append(branch_niceness) 
        return 
    for e in inbound_edges:
        calculate_tfidf(H , e[0] , shortest_path , cur_distance + 1 , branch_niceness)  



BRANCH_NICENESS = {} 
for paper in G.nodes().copy(): 

    induced_graph = set()
    induced_graph_list = list(G.in_edges(nbunch = paper))
    for e in induced_graph_list:
        induced_graph.add(e[0])

    induced_graph.add(paper)
    H = G.subgraph(induced_graph)
    print(len(H.edges()))
    if len(H.edges()) == 0:
        continue 
    shortest_path = {} 
    for e in H.nodes():
        e_list = list(H.out_edges(nbunch = e))
        if len(e_list) > 1:
            H.remove_edge(e , paper) 

    sinks = []
    for e in H.nodes():
        inbound_edges = list(H.in_edges(nbunch = e))
        if len(inbound_edges) == 0:
            sinks.append(e) 
    # print(sinks)
    all_branch_niceness = []
    for sink in sinks:
        all_shortest_paths_generator = nx.all_shortest_paths(H , source = sink , target = paper) 
        # print(list(all_shortest_paths_generator))
        for path in list(all_shortest_paths_generator):
            branch_niceness = 0
            # print(path) 
            for node in path:
                inbound_edges = len(list(H.in_edges(nbunch = node)))
                outbound_edges = len(list(H.out_edges(nbunch = node)))
                branch_niceness += 1 / (inbound_edges + outbound_edges) 
            all_branch_niceness.append(branch_niceness) 

    mean = sum(all_branch_niceness) / len(all_branch_niceness)
    # if mean > 1:
    #   print(all_branch_niceness)
    # print(all_branch_niceness)
    print("Paper {} Sum: {} Mean: {} Min: {} Max: {}".format(paper , sum(all_branch_niceness) ,mean , 
                        min(all_branch_niceness), max(all_branch_niceness)))

    BRANCH_NICENESS[paper] = all_branch_niceness 
dump_file('BRANCH_NICENESS' , BRANCH_NICENESS)