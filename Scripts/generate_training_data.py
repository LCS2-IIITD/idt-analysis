import argparse
import pickle
from get_induced_graph import build_entire_graph, get_induced_tree, get_tree_features

parser = argparse.ArgumentParser()
parser.add_argument('--branch_data', type=str)
parser.add_argument('--TOT_data', type=str)
parser.add_argument('--nonTOT_data', type=str)
parser.add_argument('--out', type=str)

args = parser.parse_args()

branch_data_all_nodes = []
with open(args.branch_data, 'rb') as f:
    branch_data_all_nodes = pickle.load(f)

TOT_papers = []
with open(args.TOT_data, 'rb') as f:
    TOT_papers = pickle.load(f)

nonTOT_papers = []
with open(args.nonTOT_data, 'rb') as f:
    nonTOT_papers = pickle.load(f)

dataset = []
i = 0
for k,v in TOT_papers.items():
    if k in branch_data_all_nodes:
        branch_list = branch_data_all_nodes[k]
        ind_tree = get_induced_tree(branch_list)
        features = get_tree_features(k, ind_tree)
        # dataset.append((int(k),features))
        dataset.append(str(k) + ' ' + ' '.join([str(fet) for fet in features]) + ' 1')
    i += 1
    # print (i)

nontot_node_set = set()
a = 0
b = 0
for k,v in nonTOT_papers.items():
    for nodeid in v:
        if nodeid in branch_data_all_nodes and nodeid not in nontot_node_set:
            branch_list = branch_data_all_nodes[nodeid]
            if len(branch_list) > 0 and len(branch_list[0]) > 1:
                ind_tree = get_induced_tree(branch_list)
                # print(nodeid)
                # print(ind_tree.nodes())
                features = get_tree_features(nodeid, ind_tree)
                dataset.append(str(nodeid) + ' ' + ' '.join([str(fet) for fet in features]) + ' 0')
                nontot_node_set.add(nodeid)
                a += 1
        else:
            b += 1

print(a, b)

data_str = '\n'.join(dataset)

with open('./data/'+args.out, 'w') as f:
    f.write(data_str)
