#Removes an edge of the cycle randomly
import networkx as nx 
import pickle
import random 
import collections
import operator
import sys
import random

def get_pickle_dump(filename):
	with open('./dumps/'+filename+'.pickle','rb') as handle:
		Variable = pickle.load(handle)
	return Variable

def dump_file(filename, Variable):
	with open('./dumps/'+filename+'.pickle','wb') as handle:
		pickle.dump(Variable,handle,protocol=pickle.HIGHEST_PROTOCOL)

random.seed(1000)
G = get_pickle_dump('G_refined_with_valid_edges')
total_edges_removed = 0
for paper in list(G.nodes()):
	print("Current Paper : {}".format(paper))
	induced_graph = set()
	induced_graph_list = G.in_edges(nbunch = paper)

	for e in induced_graph_list:
		induced_graph.add(e[0])
	induced_graph.add(paper)

	H = G.subgraph(induced_graph)
	cycle_lists = (nx.simple_cycles(H))
	# print(cycle_lists)
	for cycle_list in list(cycle_lists):
		length_of_cycle = len(cycle_list)
		if length_of_cycle <= 2:
			try:
				G.remove_edge(cycle_list[0] , cycle_list[1])
			except nx.exception.NetworkXError:
				pass 
			continue
		r = random.randint(2,length_of_cycle - 1)
		try:
			G.remove_edge(cycle_list[r- 1] , cycle_list[r])
		except nx.exception.NetworkXError:
			pass 
		print("{} {} Removed from {}".format(cycle_list[r-1] , cycle_list[r] , cycle_list))
		total_edges_removed += 1


print(total_edges_removed)
dump_file('G_without_cycles' , G)




#2791 edges removed for forward and 42 for reversed 