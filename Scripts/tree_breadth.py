import networkx as nx 
import pickle
import random 
import collections
import operator
import sys
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt 

def get_pickle_dump(filename):
	with open('./dumps/'+filename+'.pickle','rb') as handle:
		Variable = pickle.load(handle)
	return Variable

def dump_file(filename, Variable):
	with open('./dumps/'+filename+'.pickle','wb') as handle:
		pickle.dump(Variable,handle,protocol=pickle.HIGHEST_PROTOCOL)


def all_edges_in_set_A(P,n, done):
	# print("Called by {}".format(n))
	e_list = list(P.out_edges(nbunch = n))
	# print(e_list)
	for e in e_list:
		if e[1] not in done:
			return False
	return True


def get_the_latest_parent(book_keep , G, paper):
	e_list = list(G.out_edges(nbunch = paper))
	max_depth = -1
	ancestor_paper = ""
	for e in e_list:
		if book_keep[e[1]] > max_depth:
			max_depth = book_keep[e[1]]
			ancestor_paper = e[1]
	return ancestor_paper

def remove_edges_except(paper, ancestor_paper , G):
	e_list = list(G.out_edges(nbunch = paper))
	for e in e_list:
		if e[1] != ancestor_paper:
			G.remove_edge(*e) 
	return G 

def get_max_from_dict(d):
	a = [d[w] for w in d.keys()]
	a.sort(reverse = True)
	return a[0]

def get_breadth_of_each_branch(G , paper, cur_depth , breadth_info , main_paper):
	e_list = list(G.in_edges(nbunch = paper))
	try:
		breadth_info[main_paper][cur_depth] += 1
	except KeyError:
		breadth_info[main_paper][cur_depth] = 1
	if len(e_list) == 0:
		return
	for e in e_list:
		get_breadth_of_each_branch(G , e[0] , 1 + cur_depth , breadth_info ,main_paper)

def get_breadth_paper_of_each_branch(G , paper, cur_depth , breadth_info , main_paper):
	e_list = list(G.in_edges(nbunch = paper))
	try:
		breadth_info[main_paper][cur_depth].append(paper)
	except KeyError:
		breadth_info[main_paper][cur_depth] = [paper] 
	if len(e_list) == 0:
		return
	for e in e_list:
		get_breadth_paper_of_each_branch(G , e[0] , 1 + cur_depth , breadth_info ,main_paper)

# global_breadth_breadth = get_pickle_dump('global_breadth_breadth_v2') #this will contain the depth and breadth of each paper. 
BREADTH = 0
DEPTH = 1
TOTAL_CITATIONS = 2
breadth_info_paper = {}
d = 0 
G = get_pickle_dump('G_without_cycles') 

for paper in G.nodes().copy():
	breadth_info_paper[paper] = {}
	print(d)
	d += 1
	print("Current Paper : {}".format(paper))

	book_keep = {}
	induced_graph = set()
	induced_graph_list = list(G.in_edges(nbunch = paper))


	for e in induced_graph_list:
		induced_graph.add(e[0])

	induced_graph.add(paper)

	H = G.subgraph(induced_graph)
	done = set()
	not_done = set(H.nodes())
	not_done.discard(paper)
	done.add(paper)
	book_keep[paper] = 0
	counter = 1
	while(len(not_done) > 0):
		cur_visit_set = set()
		for n in not_done:
			if all_edges_in_set_A(H,n,done):
				ancestor_paper = get_the_latest_parent(book_keep , H , n)
				H = remove_edges_except(n , ancestor_paper , H)
				cur_visit_set.add(n)
				book_keep[n] = counter
		done = done.union(cur_visit_set)
		for element in cur_visit_set:
			not_done.discard(element)
		counter += 1
	get_breadth_paper_of_each_branch(H , paper , 0, breadth_info_paper , paper)
	print(breadth_info_paper[paper])



# dump_file('G_branch_data_breadth_with_papers' , breadth_info_paper)

