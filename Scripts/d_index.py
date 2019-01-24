import networkx as nx 
import pickle
import random 
import collections
import operator
import sys
from math import log10
from tree_init import all_edges_in_set_A, get_the_latest_parent, remove_edges_except

BREADTH = 0
DEPTH = 1
TOTAL_CITATIONS = 2

def remove_duplicate_branches(branch_data):
    branch_data_set = list(set([ ','.join(branch) for branch in branch_data]))
    branch_data_set = [branch for branch in branch_data_set if branch != '']
    branch_data_new = [branch.split(',') for branch in branch_data_set]
    return branch_data_new

def get_pickle_dump(filename):
    with open('./dumps/'+filename+'.pickle','rb') as handle:
        Variable = pickle.load(handle)
    return Variable

def dump_file(filename, Variable):
    with open('./dumps/'+filename+'.pickle','wb') as handle:
        pickle.dump(Variable,handle,protocol=pickle.HIGHEST_PROTOCOL)


#Old function for dindex
# def get_d_index(depth_branches):
#   length_depth_branches = [len(i) for i in depth_branches]
#   count_length = collections.Counter(length_depth_branches)
#   # print(count_length)
#   d_index = 1
#   prev = 0 
#   for k in sorted(count_length , reverse = True):
#       count_length[k] += prev 
#       prev = count_length[k]
#   # print(count_length)
#   for k in sorted(count_length):
#       if count_length[k] >= k:
#           d_index = k 
#   return d_index

def get_d_index(depth_branches):
    length_depth_branches = [len(i) for i in depth_branches]
    length_depth_branches.sort(reverse = True)
    d_index = -1
    for i in range(len(length_depth_branches)):
        if length_depth_branches[i] >= i + 1:
            d_index = i + 1
    return d_index


#Old function for d_index
# def get_d_index_till_year(depth_branches, year, paper_year_dict):
#     length_depth_branches = [len([p for p in branch if int(paper_year_dict[p]) <= year]) for branch in depth_branches]
#     count_length = collections.Counter(length_depth_branches)
#     # print(count_length)
#     d_index = 1
#     prev = 0 
#     for k in sorted(count_length , reverse = True):
#         count_length[k] += prev 
#         prev = count_length[k]
#     # print(count_length)
#     for k in sorted(count_length):
#         if count_length[k] >= k:
#             d_index = k 
#     return d_index

def get_d_index_till_year(depth_branches, year, paper_year_dict):
    depth_branches_clipd = [[p for p in branch if int(paper_year_dict[p]) <= year] for branch in depth_branches]
    depth_branches_clipd = remove_duplicate_branches(depth_branches_clipd)
    # print(year, depth_branches_clipd)
    length_depth_branches = [len(branch) for branch in depth_branches_clipd]
    count_length = collections.Counter(length_depth_branches)
    # print(count_length)
    length_depth_branches.sort(reverse = True)
    d_index = -1
    for i in range(len(length_depth_branches)):
        if length_depth_branches[i] >= i + 1:
            d_index = i + 1
    return d_index

def graph_traversal(H, cur_paper, shortest_path, cur_distance):
    inbound_edges = list(H.in_edges(nbunch = [cur_paper]))
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

tfidf = 0.0

def get_tfidf(G, cur_paper):
    global tfidf

    H = gen_cascade_tree(G, cur_paper)

    num_calls = 0
    # print("******************************{}*************************************".format(paper))
    # print(len(H.edges()))
    graph_traversal(H, cur_paper, shortest_path, 0)

    tfidf = 0.0
    calculate_tfidf(H, cur_paper, shortest_path, 0, 0)

    return tfidf

def get_tfidf_till_year(G, cur_paper, year, paper_year_dict):
    global tfidf

    H = gen_cascade_tree_till_year(G, cur_paper, year, paper_year_dict)

    num_calls = 0
    # print("******************************{}*************************************".format(paper))
    # print(len(H.edges()))
    graph_traversal(H, cur_paper, shortest_path, 0)

    tfidf = 0.0
    calculate_tfidf(H, cur_paper, shortest_path, 0, 0)

    return tfidf

def calculate_tfidf(H, cur_paper, shortest_path, cur_distance, idf):
    global tfidf

    inbound_edges = list(H.in_edges(nbunch = [cur_paper]))
    if len(inbound_edges) == 0:
        if shortest_path[cur_paper] == cur_distance:
            tfidf += cur_distance * log10(1 + (1 / (idf + 2)))
            # print(tfidf)
        return

    idf += len(inbound_edges) - 1 
    for e in inbound_edges:
        calculate_tfidf(H , e[0] , shortest_path , cur_distance + 1 , idf)

def get_tree_quality(G, cur_paper):
    H = gen_cascade_tree(G, cur_paper) 

    if len(H.edges()) == 0:
        return 0 

    sinks = []
    for e in H.nodes():
        inbound_edges = list(H.in_edges(nbunch = [e]))
        if len(inbound_edges) == 0:
            sinks.append(e) 
    # print(sinks)
    all_branch_niceness = []
    for sink in sinks:
        all_shortest_paths_generator = nx.all_shortest_paths(H , source = sink , target = cur_paper) 
        # print(len(list(all_shortest_paths_generator)))
        try:
            for path in all_shortest_paths_generator:
                branch_niceness = 0
                # print(path) 
                for node in path:
                    inbound_edges = len(list(H.in_edges(nbunch = [node])))
                    outbound_edges = len(list(H.out_edges(nbunch = [node])))
                    branch_niceness += 1 / (inbound_edges + outbound_edges) 
                all_branch_niceness.append(branch_niceness)
        except nx.exception.NetworkXNoPath as e:
            pass

    mean = sum(all_branch_niceness)
    if len(all_branch_niceness) > 0:
        mean /= len(all_branch_niceness)

    return mean

def get_tree_quality_till_year(G, cur_paper, year, paper_year_dict):
    H = gen_cascade_tree_till_year(G, cur_paper, year, paper_year_dict)

    if len(H.edges()) == 0:
        return 0

    shortest_path = {} 
    for e in H.nodes():
        e_list = list(H.out_edges(nbunch = [e]))
        if len(e_list) > 1:
            H.remove_edge(e , cur_paper) 

    sinks = []
    for e in H.nodes():
        inbound_edges = list(H.in_edges(nbunch = [e]))
        if len(inbound_edges) == 0:
            sinks.append(e) 
    # print(sinks)
    all_branch_niceness = []
    for sink in sinks:
        all_shortest_paths_generator = nx.all_shortest_paths(H , source = sink , target = cur_paper) 
        # print(len(list(all_shortest_paths_generator)))
        try:
            for path in all_shortest_paths_generator:
                branch_niceness = 0
                # print(path) 
                for node in path:
                    inbound_edges = len(list(H.in_edges(nbunch = [node])))
                    outbound_edges = len(list(H.out_edges(nbunch = [node])))
                    branch_niceness += 1 / (inbound_edges + outbound_edges) 
                all_branch_niceness.append(branch_niceness)
        except nx.exception.NetworkXNoPath as e:
            # print('conn', cur_paper, list(nx.weakly_connected_components(H)))
            # print(year, paper_year_dict[cur_paper], int(paper_year_dict[cur_paper]) <= year)
            # exit(0)
            pass

    mean = sum(all_branch_niceness)
    # if len(all_branch_niceness) > 0:
    #     mean /= len(all_branch_niceness)

    return mean

def get_tree_niceness(G, cur_paper):
    H = gen_cascade_tree(G, cur_paper)

    if len(H.edges()) == 0:
        return 0 

    nodes = list(H.nodes())
    leaf_nodes = [] 
    for v in nodes:
            in_edges = H.in_edges(nbunch = [v]) 
            if len(in_edges) == 0:
                    leaf_nodes.append(v) 
    v_count = {i : 0 for i in nodes}
    for v in leaf_nodes:
            paths = list(nx.all_shortest_paths(H , source = v , target = cur_paper)) 
            for path in paths:
                    for e in path:
                            v_count[e] += 1 

    total_niceness_inv = 0
    for i in nodes:
            total_niceness_inv += v_count[i] 

    total_niceness = 1 / total_niceness_inv
    return total_niceness

def get_tree_niceness_till_year(G, cur_paper, year, paper_year_dict):
    H = gen_cascade_tree_till_year(G, cur_paper, year, paper_year_dict)

    # print('Root', cur_paper, 'Year', year)
    # print(H.edges())
    # print('Pubs', [(n, paper_year_dict[n]) for n in H.nodes() if n in paper_year_dict])

    if len(H.edges()) == 0:
        return 0

    # print(list(H.edges()))

    nodes = list(H.nodes())
    leaf_nodes = [] 
    for v in nodes:
        in_edges = H.in_edges(nbunch = [v]) 
        if len(in_edges) == 0:
            leaf_nodes.append(v) 
    v_count = {i : 0 for i in nodes}
    for v in leaf_nodes:
        paths = list(nx.all_shortest_paths(H , source = v , target = cur_paper)) 
        for path in paths:
                for e in path:
                    v_count[e] += 1 

    # print('Counter', v_count)

    total_niceness_inv = 0
    for i in nodes:
        if i != cur_paper:
            total_niceness_inv += v_count[i] 

    total_niceness = 1 / total_niceness_inv
    # print('Niceness', total_niceness)
    return total_niceness

def gen_cascade_tree(G, cur_paper):
    induced_graph = set()
    induced_graph_list = list(G.in_edges(nbunch = [cur_paper]))
    for e in induced_graph_list:
        induced_graph.add(e[0])

    induced_graph.add(cur_paper)
    H = G.subgraph(induced_graph)
    # print(len(H.edges()))
    shortest_path = {} 
    for e in H.nodes():
        e_list = list(H.out_edges(nbunch = [e]))
        if len(e_list) > 1:
            H.remove_edge(e , cur_paper)
    return H

def gen_cascade_tree_till_year(G, cur_paper, year, paper_year_dict):
    induced_graph = set()
    induced_graph_list = list(G.in_edges(nbunch = [cur_paper]))

    # if cur_paper == '577414':
    #     print('No of in-edges', len(induced_graph_list))
    for e in induced_graph_list:
        if e[0] in paper_year_dict and int(paper_year_dict[e[0]]) <= year:
            induced_graph.add(e[0])
        elif e[0] not in paper_year_dict:
            print('found!')

    induced_graph.add(cur_paper)
    H = G.subgraph(induced_graph)
    # print(len(H.edges()))

    # if cur_paper == '577414':
    #     print(len(H.nodes()), len(H.edges()))
        # print(H.nodes())
        # print(H.edges())

    shortest_path = {} 
    for e in H.nodes():
        e_list = list(H.out_edges(nbunch = [e]))
        if len(e_list) > 1:
            H.remove_edge(e , cur_paper)

    return H

def gen_actual_cascade_tree(G, cur_paper):
    induced_graph = set()
    induced_graph_list = list(G.in_edges(nbunch = [cur_paper]))

    for e in induced_graph_list:
        induced_graph.add(e[0])
    induced_graph.add(cur_paper)

    H = G.subgraph(induced_graph)
    book_keep = {}
    done = set()
    not_done = set(H.nodes())
    not_done.discard(cur_paper)
    done.add(cur_paper)
    book_keep[cur_paper] = 0
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
    return H

def gen_actual_cascade_tree_till_year(G, cur_paper, year, paper_year_dict):
    induced_graph = set()
    induced_graph_list = list(G.in_edges(nbunch = [cur_paper]))

    for e in induced_graph_list:
        if e[0] in paper_year_dict and int(paper_year_dict[e[0]]) <= year:
            induced_graph.add(e[0])
        elif e[0] not in paper_year_dict:
            print('found!')
    induced_graph.add(cur_paper)

    H = G.subgraph(induced_graph)
    book_keep = {}
    done = set()
    not_done = set(H.nodes())
    not_done.discard(cur_paper)
    done.add(cur_paper)
    book_keep[cur_paper] = 0
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
    return H

# if __name__ == "__main__":
#   D_INDEX_DICT = {}
#   d = get_pickle_dump('G_branch_data_depth')
#   for k in d:
#       d_index = get_d_index(d[k])
#       D_INDEX_DICT[k] = d_index
#       print("{} PAPER {} D INDEX".format(k , d_index))
#   dump_file('D_INDEX_DICT' , D_INDEX_DICT)