import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from d_index import gen_cascade_tree, gen_cascade_tree_till_year, get_tree_niceness
from d_index import gen_actual_cascade_tree, gen_actual_cascade_tree_till_year

import os
import argparse
import pickle
import numpy as np
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

parser = argparse.ArgumentParser()
parser.add_argument('--branch_data', type=str)
parser.add_argument('--dir', type=str)
parser.add_argument('--g', type=int)

args = parser.parse_args()

G = nx.DiGraph()
with open(args.branch_data, 'rb') as f:
    G = pickle.load(f)

print("graph loaded!")

paper_year_dict = {}
with open('./data/PAPER_YEAR_DICT.pickle', 'rb') as f:
    paper_year_dict = pickle.load(f)

paper_cum_citation_dict = {}
with open('./data/CUMMULATIVE_CITATIONS_ENRICHED.pickle', 'rb') as f:
    paper_cum_citation_dict = pickle.load(f)

conference_paper_list_dict = {}
with open('./data/CONF_PAPERS_DICT2.pkl', 'rb') as f:
    conference_paper_list_dict = pickle.load(f)

TOTpaper_venue_dict = {}
with open('./data/YEAR_VENUE_OF_AWARD_DICT.pickle', 'rb') as f:
    TOTpaper_venue_dict = pickle.load(f)

TOT_conf_set = set([TOTpaper_venue_dict[paper]['VENUE'] for paper in TOTpaper_venue_dict])

def plot_tree_pygraphviz(H, node_labels, fname):
	pos = graphviz_layout(H, prog='dot')
	fname = fname.replace('.', '__')
	#print(fname)
	nx.draw(G=H, pos=pos, labels=node_labels, arrows=False)
	plt.savefig(fname, bbox_inches='tight')
	plt.close()

def compare_tot_neighbour():
    i = 0
    for tot_paper, tot_paper_data in TOTpaper_venue_dict.items():
        venue = tot_paper_data['VENUE']
        conf_year = int(tot_paper_data['PUBLISHED'])
        rest_papers = conference_paper_list_dict[venue][str(conf_year)]
        rest_papers = [paper for paper in rest_papers if paper in paper_cum_citation_dict]
        rest_papers.sort(key=lambda x: (-paper_cum_citation_dict[x][max([k for k in paper_cum_citation_dict[x]])]))

        try:
            tot_paper_index = [i for i,paper in enumerate(rest_papers) if paper == tot_paper][0]
            # print('found')
        except IndexError as ie:
            print(':(')
            continue

        H = gen_actual_cascade_tree_till_year(G, tot_paper, conf_year + 5, paper_year_dict)
        no_labelsh = {}
        for no in H.nodes():
            # print(no)
            no_labelsh[no] = ''
        no_labelsh[tot_paper] = 'R'
        H.reverse()

        i_index = tot_paper_index + 1
        I = gen_cascade_tree_till_year(G, rest_papers[i_index], conf_year + 5, paper_year_dict)
        no_labelsi = {}
        for no in I.nodes():
            no_labelsi[no] = ''
        no_labelsi[rest_papers[i_index]] = 'R'
        I.reverse()

        J = None
        j_index = -1
        if tot_paper_index == 0:
            j_index = tot_paper_index + 2
        else:
            j_index = tot_paper_index - 1
        J = gen_cascade_tree_till_year(G, rest_papers[j_index], conf_year + 5, paper_year_dict)
        no_labelsj = {}
        for no in J.nodes():
            no_labelsj[no] = ''
        no_labelsj[rest_papers[j_index]] = 'R'
        J.reverse()

        # fig, ax = plt.subplots()
        # nx.draw(H, ax=ax)

        #posh = graphviz_layout(H, prog='dot')
        #nx.draw(G=H, pos=posh, labels=no_labelsh, arrows=False)
        #plt.savefig(args.dir + '/' + tot_paper + '_' + str(len(list(H.nodes()))-1) + '_tot', bbox_inches='tight')
        #plt.close()
        plot_tree_pygraphviz(H, no_labelsh, args.dir + '/' + tot_paper + '_' + str(len(list(H.nodes()))-1) + '_tot')

        # posi = graphviz_layout(I, prog='dot')
        # nx.draw(G=I, pos=posi, labels=no_labelsi, arrows=False)
        # plt.savefig(args.dir + '/' + tot_paper + '_' + str(len(list(I.nodes()))-1) + '_i', bbox_inches='tight')
        # plt.close()
        plot_tree_pygraphviz(I, no_labelsi, args.dir + '/' + tot_paper + '_' + str(len(list(I.nodes()))-1) + '_i')

        # posj = graphviz_layout(J, prog='dot')
        # nx.draw(G=J, pos=posj, labels=no_labelsj, arrows=False)
        # plt.savefig(args.dir + '/' + tot_paper + '_' + str(len(list(J.nodes()))-1) + '_j', bbox_inches='tight')
        # plt.close()
        plot_tree_pygraphviz(J, no_labelsj, args.dir + '/' + tot_paper + '_' + str(len(list(J.nodes()))-1) + '_j')

        print(i, len(list(H.nodes())), len(list(I.nodes())), len(list(J.nodes())))
        i += 1

        # break

def visualise_by_gain_bucketing():
    all_papers_data = []
    with open('./gain_all_papers') as f:
        all_papers_data = f.readlines()
    all_papers_data = [line.split('\t') for line in all_papers_data]
    all_papers_data = [(paper, int(cit5), int(cit10), float(nice)) for paper, cit5, cit10, nice in all_papers_data]
    citation5_data = [paper_data[1] for paper_data in all_papers_data]

    num_bins = 10
    _, bin_edges = np.histogram(citation5_data, bins=num_bins)
    print(bin_edges)

    bins = [[] for i in range(num_bins)]

    for paper_data in all_papers_data:
        cit5 = paper_data[1]
        for i in range(1, len(bin_edges)):
            left = bin_edges[i-1]
            right = bin_edges[i]
            if cit5 >= left and cit5 < right:
                bins[i-1].append(paper_data)
                break

    for i,paper_group in enumerate(bins[args.g : args.g + 1]):
        # print(paper_group)
        # break
        group_cit_data = [paper_data[1] for paper_data in paper_group]
        cit_mean = np.mean(group_cit_data)
        cit_std = np.std(group_cit_data)
        cit_min = np.min(group_cit_data)
        cit_max = np.max(group_cit_data)
        print(i, len(paper_group), cit_mean, cit_std, cit_min, cit_max)

        save_dir = args.dir + '/' + str(i)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        with open(save_dir + '/metadata.txt', 'w') as f:
            f.write(
                    'Mean = ' + str(cit_mean) + '\n' +
                    'Std = ' + str(cit_std) + '\n' +
                    'Min = ' + str(cit_min) + '\n' +
                    'Max = ' + str(cit_max)
                    )

        for paper_data in paper_group:
            cit5 = paper_data[1]
            cit10 = paper_data[2]
            gain = (cit10 - cit5) / float(cit5 + 1)

            tree_save_dir = save_dir + '/gain_more_than_50'
            if gain <= 0.1:
                tree_save_dir = save_dir + '/gain_less_than_10'
            
            if not os.path.exists(tree_save_dir):
                os.makedirs(tree_save_dir)
            
            if cit5 > 0 and cit10 > 0:
                cur_paper = paper_data[0]
                niceness = paper_data[3]
                pub_year = int(paper_year_dict[cur_paper])
                H = gen_actual_cascade_tree_till_year(G, cur_paper, pub_year + 5, paper_year_dict)
                no_labels = {}
                for no in H.nodes():
                    # print(no)
                    no_labels[no] = ''
                no_labels[cur_paper] = 'R'
                H.reverse()
                plot_tree_pygraphviz(H, no_labels, tree_save_dir + '/' + str(cur_paper) + '_' + str(gain) + '_' + str(niceness))



# compare_tot_neighbour()
visualise_by_gain_bucketing()
