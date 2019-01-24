import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import argparse
import pickle
import numpy as np
import networkx as nx

from d_index import gen_cascade_tree, gen_cascade_tree_till_year, get_tree_niceness, get_tree_niceness_till_year
from ranking import get_tniceness_ranklist, get_citation_ranklist, get_delta_citation_ranklist, get_ideal_tniceness_distance_ranklist

parser = argparse.ArgumentParser()
parser.add_argument('--branch_data', type=str)
parser.add_argument('--out', type=str)

args = parser.parse_args()

def niceness_rank_tot():
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

    paper_conference_dict = {}
    with open('./data/PAPER_VENUE_DICT_CONF.pickle', 'rb') as f:
        paper_conference_dict = pickle.load(f)

    conference_paper_list_dict = {}
    with open('./data/CONF_PAPERS_DICT2.pkl', 'rb') as f:
        conference_paper_list_dict = pickle.load(f)

    TOTpaper_venue_dict = {}
    with open('./data/YEAR_VENUE_OF_AWARD_DICT.pickle', 'rb') as f:
        TOTpaper_venue_dict = pickle.load(f)

    TOT_paper_set = set([paper for paper in TOTpaper_venue_dict])
    TOT_conf_set = set([TOTpaper_venue_dict[paper]['VENUE'] for paper in TOTpaper_venue_dict])


    yvals = []
    yvals2 = []
    count = 0
    for tot_paper, tot_paper_data in TOTpaper_venue_dict.items():
        conf_year = int(tot_paper_data['PUBLISHED'])
        count += 1
        if conf_year > 2005:
            count -= 1
            continue
        venue = tot_paper_data['VENUE']
        paper_list = conference_paper_list_dict[venue][str(conf_year)]
        paper_list = [paper for paper in paper_list if paper in paper_cum_citation_dict]
        # print(len(paper_list))
        # paper_list.sort(key=lambda x: paper_cum_citation_dict[x][max([year for year in paper_cum_citation_dict[x]])], reverse=True)
        paper_list.sort(key=lambda x: paper_cum_citation_dict[x][min(conf_year + 5, max([year for year in paper_cum_citation_dict[x]]))], reverse=True)
        # print(len(paper_list), [i for i,paper in enumerate(paper_list) if paper == tot_paper])
        top_paper_list = paper_list[:max(5, int(0.05 * len(paper_list)))]
                
        # print(paper_list[0], type(paper_list[0]))
        # print(type(list(TOT_conf_set)[0]))
        try:
            tot_paper_index = [i for i,paper in enumerate(top_paper_list) if paper == tot_paper][0]
            # print('found')
        except IndexError as ie:
            print(':(')
            continue
        # print('Okay')
        ndict, niceness_ranklist = get_tniceness_ranklist(G, top_paper_list, conf_year + 5, paper_year_dict, paper_cum_citation_dict)
        # ndict, niceness_ranklist = get_ideal_tniceness_distance_ranklist(G, top_paper_list, conf_year + 5, paper_year_dict, paper_cum_citation_dict)
        tot_paper_rank = niceness_ranklist[tot_paper_index] + 1
        yvals.append(tot_paper_rank)
        cit_rank = [i for i,paper in enumerate(paper_list) if paper == tot_paper][0] + 1
        yvals2.append(cit_rank)
        if abs(tot_paper_rank - cit_rank) > 10:
            print('tot = ', paper_cum_citation_dict[tot_paper][max([int(year) for year in paper_cum_citation_dict[paper_list[tot_paper_index]]])])
            if tot_paper_index == 0:
                print('oth1 = ', paper_cum_citation_dict[paper_list[tot_paper_index + 1]][max([int(year) for year in paper_cum_citation_dict[paper_list[tot_paper_index + 1]]])])
                print('oth2 = ', paper_cum_citation_dict[paper_list[tot_paper_index + 2]][max([int(year) for year in paper_cum_citation_dict[paper_list[tot_paper_index + 2]]])])
            else:
                print('oth1 = ', paper_cum_citation_dict[paper_list[tot_paper_index - 1]][max([int(year) for year in paper_cum_citation_dict[paper_list[tot_paper_index - 1]]])])
                print('oth2 = ', paper_cum_citation_dict[paper_list[tot_paper_index + 1]][max([int(year) for year in paper_cum_citation_dict[paper_list[tot_paper_index + 1]]])])


    # exit(0)
    xind = np.arange(len(yvals))
    width = 0.4
    fig, ax = plt.subplots()
    if 'dist' in args.out:
        ax.bar(xind, yvals, width=width, label='Ideal-dist')
    else:
        ax.bar(xind, yvals, width=width, label='Niceness')
    ax.bar(xind + width, yvals2, width=width, label='Citations')
    ax.set_xlabel('TOT Paper')
    ax.legend()
    fig.savefig(args.out, bbox_inches='tight')

def find_tot_closest_score():
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

    paper_conference_dict = {}
    with open('./data/PAPER_VENUE_DICT_CONF.pickle', 'rb') as f:
        paper_conference_dict = pickle.load(f)

    conference_paper_list_dict = {}
    with open('./data/CONF_PAPERS_DICT2.pkl', 'rb') as f:
        conference_paper_list_dict = pickle.load(f)

    TOTpaper_venue_dict = {}
    with open('./data/YEAR_VENUE_OF_AWARD_DICT.pickle', 'rb') as f:
        TOTpaper_venue_dict = pickle.load(f)

    TOT_paper_set = set([paper for paper in TOTpaper_venue_dict])
    TOT_conf_set = set([TOTpaper_venue_dict[paper]['VENUE'] for paper in TOTpaper_venue_dict])



    score = 0
    count = 0
    nontop = 0
    num_tot_papers = 0
    for tot_paper, tot_paper_data in TOTpaper_venue_dict.items():
        conf_year = int(tot_paper_data['PUBLISHED'])
        award_year = int(tot_paper_data['YEAR OF AWARD'])
        count += 1
        # if conf_year > 2010:
        #     count -= 1
        #     continue
        venue = tot_paper_data['VENUE']
        paper_list = conference_paper_list_dict[venue][str(conf_year)]
        paper_list = [paper for paper in paper_list if paper in paper_cum_citation_dict]
        # print(len(paper_list))
        # paper_list.sort(key=lambda x: paper_cum_citation_dict[x][max([year for year in paper_cum_citation_dict[x]])], reverse=True)
        paper_list.sort(key=lambda x: paper_cum_citation_dict[x][max([year for year in paper_cum_citation_dict[x]])], reverse=True)
        # print(len(paper_list), [i for i,paper in enumerate(paper_list) if paper == tot_paper])
        # top_paper_list = paper_list[:max(5, int(0.05 * len(paper_list)))]
                
        # print(paper_list[0], type(paper_list[0]))
        # print(type(list(TOT_conf_set)[0]))
        try:
            tot_paper_index = [i for i,paper in enumerate(paper_list) if paper == tot_paper][0]
            # print('found')
        except IndexError as ie:
            print(':(')
            continue
        # print('Okay')

        closest1 = tot_paper_index + 1
        closest = tot_paper_index + 1
        if tot_paper_index == len(paper_list) - 1:
            closest = tot_paper_index - 1
        elif tot_paper_index != 0:
            closest2 = tot_paper_index - 1
            closest2_paper = paper_list[closest2]
            closest1_paper = paper_list[closest1]
            tot_cits = paper_cum_citation_dict[tot_paper][min(award_year, max([year for year in paper_cum_citation_dict[tot_paper]]))]
            closest = min( (abs(paper_cum_citation_dict[closest1_paper][min(award_year, max([year for year in paper_cum_citation_dict[closest1_paper]]))] - tot_cits), closest1),
                            (abs(paper_cum_citation_dict[closest2_paper][min(award_year, max([year for year in paper_cum_citation_dict[closest2_paper]]))] - tot_cits), closest2) )[1]


        ndict, niceness_ranklist = get_tniceness_ranklist(G, paper_list, paper_cum_citation_dict)
        # ndict, niceness_ranklist = get_ideal_tniceness_distance_ranklist(G, paper_list, paper_cum_citation_dict)
        tot_paper_rank = niceness_ranklist[tot_paper_index] + 1
        closest_rank = niceness_ranklist[closest] + 1
        
        cit_rank = [i for i,paper in enumerate(paper_list) if paper == tot_paper][0] + 1
        
        if tot_paper_rank <= closest_rank:
            score += 1
        if cit_rank != 1:
            nontop += 1

        num_tot_papers += 1

    print(score, num_tot_papers, nontop)

def find_citation_gain_50(total_count = 10000000000):
    G = nx.DiGraph()
    with open(args.branch_data, 'rb') as f:
        G = pickle.load(f)

    paper_year_dict = {}
    with open('./data/PAPER_YEAR_DICT.pickle', 'rb') as f:
        paper_year_dict = pickle.load(f)

    paper_cum_citation_dict = {}
    with open('./data/CUMMULATIVE_CITATIONS_ENRICHED.pickle', 'rb') as f:
        paper_cum_citation_dict = pickle.load(f)

    count = 0
    write_data = []
    # print(len([paper for paper in paper_cum_citation_dict if int(paper_year_dict[paper]) < 2001]))
    for paper, cit_data in paper_cum_citation_dict.items():
        if count < total_count and paper in paper_year_dict:
            pub_year = int(paper_year_dict[paper])
            if pub_year < 2001:
                cit_5 = cit_data[pub_year + 5]
                cit_10 = cit_data[pub_year + 10]
                gain = (cit_10 - cit_5) / (cit_5 + 1)
                # print(gain)
                if gain <= 0.2 and cit_10 > 0:
                    nice = get_tree_niceness_till_year(G, paper, pub_year + 5, paper_year_dict)
                    write_data.append(paper + '\t' + str(cit_5) + '\t' + str(cit_10) + '\t' + str(nice))

                    count += 1

    write_data_str = '\n'.join(write_data)
    with open(args.out, 'w') as f:
        f.write(write_data_str) 


# niceness_rank_tot()
# find_tot_closest_score()
find_citation_gain_50()
# print(paper_cum_citation_dict['4523'])
# print(TOTpaper_venue_dict['4523'])
# print(paper_conference_dict['4523'])
# print(paper_year_dict['4523'])
# print([paper_year_dict[paper] for paper in conference_paper_list_dict['1652'] if paper in paper_year_dict])