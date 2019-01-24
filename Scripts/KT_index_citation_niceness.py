import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle
import numpy as np
import argparse
from ranking import get_tniceness_ranklist, get_citation_ranklist, get_delta_citation_ranklist
from d_index import gen_cascade_tree, get_tree_niceness
from scipy.stats import kendalltau
import networkx as nx

parser = argparse.ArgumentParser()
parser.add_argument('--branch_data', type=str)
parser.add_argument('--out', type=str)

args = parser.parse_args()

G = None
with open(args.branch_data, 'rb') as f:
    G = pickle.load(f)

print("graph loaded!")

paper_conference_dict = {}
with open('./data/PAPER_VENUE_DICT_CONF.pickle', 'rb') as f:
    paper_conference_dict = pickle.load(f)

conference_paper_list_dict = {}
with open('./data/CONF_PAPERS_DICT.pickle', 'rb') as f:
    conference_paper_list_dict = pickle.load(f)

paper_year_dict = {}
with open('./data/PAPER_YEAR_DICT.pickle', 'rb') as f:
    paper_year_dict = pickle.load(f)

paper_cum_citation_dict = {}
with open('./data/CUMMULATIVE_CITATIONS_ENRICHED.pickle', 'rb') as f:
    paper_cum_citation_dict = pickle.load(f)

TOTpaper_venue_dict = {}
with open('./data/YEAR_VENUE_OF_AWARD_DICT.pickle', 'rb') as f:
    TOTpaper_venue_dict = pickle.load(f)

TOT_conf_set = set([TOTpaper_venue_dict[paper]['VENUE'] for paper in TOTpaper_venue_dict])

def find_best_subset(paper_list, paper_cum_citation_dict, tol=0.1):
    all_best_sets = []
    cur_set = [paper_list[0]]
    for i in range(1, len(paper_list)):
        cur_paper = paper_list[i]
        cur_last_year = max([int(year) for year in paper_cum_citation_dict[cur_paper]])
        prev_paper = paper_list[i-1]
        prev_last_year = max([int(year) for year in paper_cum_citation_dict[prev_paper]])
        fall = -(paper_cum_citation_dict[cur_paper][cur_last_year] - paper_cum_citation_dict[prev_paper][prev_last_year]) / float(paper_cum_citation_dict[prev_paper][prev_last_year])
        # print(fall)
        if fall <= tol:
            cur_set.append(cur_paper)
        else:
            all_best_sets.append(cur_set)
            cur_set = [cur_paper]
    if len(cur_set) > 0:
        all_best_sets.append(cur_set)
    all_best_sets.sort(key=lambda x: -len(x))
    return all_best_sets[0]

yvals = []
xticks = []
positive_confs = []
numbers = [0, 0]

all_corrs = []

# H = gen_cascade_tree(G, '349826')
# print(nx.is_tree(H))
# print(H.edges())
# print([(node, paper_year_dict[node]) for node in H.nodes()])
# print(get_tree_niceness(H, '349826'))
# exit(0)

for conference, paper_list in conference_paper_list_dict.items():
    conf_year = -1
    for i in range(len(paper_list)):
        if paper_list[0] in paper_year_dict:
            conf_year = int(paper_year_dict[paper_list[0]])
            break

    # if conf_year >= 1995 and conf_year <= 2000 and (conference in TOT_conf_set):
    if conf_year >= 1995 and conf_year <= 2000:

        paper_list = [paper for paper in paper_list if paper in paper_cum_citation_dict]

        # paper_list = sorted( paper_list, key=lambda x: (paper_cum_citation_dict[x][max([k for k in paper_cum_citation_dict[x]])] if x in paper_cum_citation_dict else 0) ) [int(0.95 * len(paper_list)):]
        paper_list = sorted( paper_list, key=lambda x: (-paper_cum_citation_dict[x][max([k for k in paper_cum_citation_dict[x]])] if x in paper_cum_citation_dict else 0) ) [:int(0.05 * len(paper_list))]
        # paper_list = sorted( paper_list, key=lambda x: (-paper_cum_citation_dict[x][max([k for k in paper_cum_citation_dict[x]])]) )

        # paper_list = find_best_subset(paper_list, paper_cum_citation_dict)
        # continue

        if len(paper_list) < 3:
            continue

        # print([paper_cum_citation_dict[paper][max([k for k in paper_cum_citation_dict[paper]])] for paper in paper_list])
        # continue

        # print(conference)

        # d_index_dict5, d_rank5 = get_d_index_ranklist(paper_list, conf_year + 5, paper_branch_data, paper_year_dict, paper_cum_citation_dict)
        # d_index_dict5, d_rank5 = get_tfidf_ranklist(G, paper_list, conf_year + 5, paper_year_dict, paper_cum_citation_dict)
        # d_index_dict5, d_rank5 = get_tniceness_ranklist(G, paper_list, conf_year + 5, paper_year_dict, paper_cum_citation_dict)
        # print()
        # d_index_dict10, d_rank10 = get_d_index_ranklist(paper_list, conf_year + 10, paper_branch_data, paper_year_dict, paper_cum_citation_dict)
        # d_index_dict10, d_rank10 = get_tfidf_ranklist(G, paper_list, conf_year + 10, paper_year_dict, paper_cum_citation_dict)
        # d_index_dict10, d_rank10 = get_tniceness_ranklist(G, paper_list, conf_year + 10, paper_year_dict, paper_cum_citation_dict)
        # print()

        d_index_dict5 = {}
        c_rank5 = get_citation_ranklist(paper_list, conf_year + 5, paper_cum_citation_dict, paper_year_dict, d_index_dict5)
        # print()
        d_index_dict10 = {}
        # c_rank10 = get_citation_ranklist(paper_list, conf_year + 10, paper_cum_citation_dict, paper_year_dict, d_index_dict5)
        c_rank10 = get_delta_citation_ranklist(paper_list, conf_year + 5, conf_year + 10, paper_cum_citation_dict, paper_year_dict, d_index_dict5)
        # print()

        # print(len(d_rank5), len(d_rank5), len(c_rank5), len(c_rank10))
        # print(d_rank_correlation, c_rank_correlation)

        # if np.isnan(d_rank_correlation) or np.isnan(c_rank_correlation):
            # continue

        # corr, pval = kendalltau(d_rank5, c_rank10)
        corr, pval = kendalltau(c_rank5, c_rank10)
        if np.isnan(corr) or np.isnan(pval):
            print(':(')
            continue

        yvals.append(corr)
        # yvals.append(d_rank_correlation)

        # if d_rank_correlation > c_rank_correlation:
        #     positive_confs.append(conference)
        #     numbers[0] += 1
        # else:
        #     numbers[1] += 1

        # print(d_rank_correlation, c_rank_correlation)
        # exit(0)

#print(numbers)
# positive_confs = '\n'.join(positive_confs)
# with open('positive_confs', 'w') as f:
#     f.write(positive_confs)

# exit(0)
print(len(yvals))
print(sum(yvals)/float(len(yvals)))

plt.bar(range(len(yvals)), yvals)
plt.xlabel('Conference')
# plt.ylabel('Kendall-Tau (niceness-after-5, delta-citations-at-5-10')
# plt.ylabel('Kendall-Tau (niceness-after-5, citations-at-10')
# plt.title('Kendall-Tau Correlation between Tree niceness at 5 years and delta citations at 5,10 years')
# plt.title('Kendall-Tau Correlation between Tree niceness at 5 years and citations at 10 years')
plt.savefig(args.out, bbox_inches='tight')