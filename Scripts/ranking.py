from d_index import get_d_index, get_d_index_till_year, get_tfidf, get_tfidf_till_year
from d_index import get_tree_quality, get_tree_quality_till_year, get_tree_niceness, get_tree_niceness_till_year
import numpy as np
from scipy.stats import spearmanr
import math

def get_d_index_ranklist(paper_list, year, paper_branch_data, paper_year_dict, paper_cum_citation_dict):
    d_index_list = [(get_d_index_till_year(paper_branch_data[paper], year, paper_year_dict),i) if paper in paper_branch_data else (0,i) for i,paper in enumerate(paper_list)]
    d_index_list.sort(reverse=True)
    ranklist = [0] * len(paper_list)
    rank = 0
    prevDIndex = float('inf')
    # print(d_index_list)
    for i,data in enumerate(d_index_list[1:]):
        if data[0] < prevDIndex:
            rank += 1
        ranklist[data[1]] = rank
        prevDIndex = data[0]

    # print(ranklist)
    # print([(data[0], paper_list[data[1]], paper_cum_citation_dict[paper_list[data[1]]][year]) for data in d_index_list[:10]])

    d_index_dict = {data[1]:data[0] for data in d_index_list}
    return d_index_dict, ranklist

def get_tfidf_ranklist(G, paper_list, year, paper_year_dict, paper_cum_citation_dict):
    # d_index_list = [(get_tfidf(G, paper),i) for i,paper in enumerate(paper_list)]
    d_index_list = [(get_tfidf_till_year(G, paper, year, paper_year_dict),i) for i,paper in enumerate(paper_list)]
    d_index_list.sort(reverse=True)
    ranklist = [0] * len(paper_list)
    rank = 0
    prevDIndex = float('inf')
    # print(d_index_list)
    for i,data in enumerate(d_index_list[1:]):
        if data[0] < prevDIndex:
            rank += 1
        ranklist[data[1]] = rank
        prevDIndex = data[0]

    # print(ranklist)
    # print([(data[0], paper_list[data[1]], paper_cum_citation_dict[paper_list[data[1]]][year]) for data in d_index_list[:10]])

    d_index_dict = {data[1]:data[0] for data in d_index_list}
    return d_index_dict, ranklist

def get_tquality_ranklist(G, paper_list, year, paper_year_dict, paper_cum_citation_dict):
    # d_index_list = [(get_tree_quality(G, paper), i) for i,paper in enumerate(paper_list)]
    d_index_list = [(get_tree_quality_till_year(G, paper, year, paper_year_dict), i) for i,paper in enumerate(paper_list) if paper in paper_year_dict]
    d_index_list.sort(reverse=True)
    ranklist = [0] * len(paper_list)
    rank = 0
    prevDIndex = float('inf')
    # print(d_index_list)
    for i,data in enumerate(d_index_list[1:]):
        if data[0] < prevDIndex:
            rank += 1
        ranklist[data[1]] = rank
        prevDIndex = data[0]

    # print(ranklist)
    # print([(data[0], paper_list[data[1]], paper_cum_citation_dict[paper_list[data[1]]][year]) for data in d_index_list[:10]])

    d_index_dict = {data[1]:data[0] for data in d_index_list}
    return d_index_dict, ranklist

def get_tniceness_ranklist(G, paper_list, paper_cum_citation_dict):
    # d_index_list = [(get_tree_quality(G, paper), i) for i,paper in enumerate(paper_list)]
    d_index_list = [(get_tree_niceness(G, paper), i) for i,paper in enumerate(paper_list)]
    d_index_list.sort(reverse=True)
    ranklist = [0] * len(paper_list)
    rank = 0
    prevDIndex = float('inf')
    # print(d_index_list)
    for i,data in enumerate(d_index_list[1:]):
        if data[0] < prevDIndex:
            rank += 1
        ranklist[data[1]] = rank
        prevDIndex = data[0]

    # print(ranklist)
    # print([(data[0], paper_list[data[1]], paper_cum_citation_dict[paper_list[data[1]]][max([year for year in paper_cum_citation_dict[x]])]) for data in d_index_list[:10]])

    d_index_dict = {data[1]:data[0] for data in d_index_list}
    return d_index_dict, ranklist

def get_tniceness_ranklist_till_year(G, paper_list, year, paper_year_dict, paper_cum_citation_dict):
    # d_index_list = [(get_tree_quality(G, paper), i) for i,paper in enumerate(paper_list)]
    d_index_list = [(get_tree_niceness_till_year(G, paper, year, paper_year_dict), i) for i,paper in enumerate(paper_list) if paper in paper_year_dict]
    d_index_list.sort(reverse=True)
    ranklist = [0] * len(paper_list)
    rank = 0
    prevDIndex = float('inf')
    # print(d_index_list)
    for i,data in enumerate(d_index_list[1:]):
        if data[0] < prevDIndex:
            rank += 1
        ranklist[data[1]] = rank
        prevDIndex = data[0]

    # print(ranklist)
    # print([(data[0], paper_list[data[1]], paper_cum_citation_dict[paper_list[data[1]]][year]) for data in d_index_list[:10]])

    d_index_dict = {data[1]:data[0] for data in d_index_list}
    return d_index_dict, ranklist

def get_ideal_tniceness(n):
    return float(1)/n
    # return n

def get_worst_tniceness(n):
    return float(1)/((n - int(n/2))*(1 + int(n/2)))
    # return (n - int(n/2))*(float(1 + int(n/2)))

def normalized_ideal_distance(tnice, n):
    # print(n, get_ideal_tniceness(n), get_worst_tniceness(n))
    if n > 3:
        return abs(get_ideal_tniceness(n) - tnice)/float(abs(get_ideal_tniceness(n) - get_worst_tniceness(n)))
    return 0.0

def get_ideal_tniceness_distance_ranklist(G, paper_list, paper_cum_citation_dict):
    # d_index_list = [(get_tree_quality(G, paper), i) for i,paper in enumerate(paper_list)]
    d_index_list = [(normalized_ideal_distance(get_tree_niceness(G, paper), paper_cum_citation_dict[paper][max([year for year in paper_cum_citation_dict[paper]])]), i) for i,paper in enumerate(paper_list)]
    d_index_list.sort()
    ranklist = [0] * len(paper_list)
    rank = 0
    prevDIndex = float('inf')
    # print(d_index_list)
    for i,data in enumerate(d_index_list[1:]):
        if data[0] > prevDIndex:
            rank += 1
        ranklist[data[1]] = rank
        prevDIndex = data[0]

    # print(ranklist)
    # print([(data[0], paper_list[data[1]], paper_cum_citation_dict[paper_list[data[1]]][year]) for data in d_index_list[:10]])

    d_index_dict = {data[1]:data[0] for data in d_index_list}
    return d_index_dict, ranklist

def get_ideal_tniceness_distance_ranklist_till_year(G, paper_list, year, paper_year_dict, paper_cum_citation_dict):
    # d_index_list = [(get_tree_quality(G, paper), i) for i,paper in enumerate(paper_list)]
    d_index_list = [(normalized_ideal_distance(get_tree_niceness_till_year(G, paper, year, paper_year_dict), paper_cum_citation_dict[paper][year]), i) for i,paper in enumerate(paper_list) if paper in paper_year_dict]
    d_index_list.sort()
    ranklist = [0] * len(paper_list)
    rank = 0
    prevDIndex = float('inf')
    # print(d_index_list)
    for i,data in enumerate(d_index_list[1:]):
        if data[0] > prevDIndex:
            rank += 1
        ranklist[data[1]] = rank
        prevDIndex = data[0]

    # print(ranklist)
    # print([(data[0], paper_list[data[1]], paper_cum_citation_dict[paper_list[data[1]]][year]) for data in d_index_list[:10]])

    d_index_dict = {data[1]:data[0] for data in d_index_list}
    return d_index_dict, ranklist

def get_citation_ranklist(paper_list, year, paper_cum_citation_dict, paper_year_dict, d_index_dict):
    # citation_list = []
    # for i,paper in enumerate(paper_list):
    #     if paper in paper_cum_citation_dict and year in paper_cum_citation_dict[paper]:
    #         print(paper_cum_citation_dict[paper])
    #         citation_list.append((paper_cum_citation_dict[paper][year], i))
    #     else:
    #         citation_list.append((0,i))

    # print(len([paper for paper in paper_list if paper in paper_cum_citation_dict]))
    # exit(0)
    citation_list = [(paper_cum_citation_dict[paper][year], i) if paper in paper_cum_citation_dict and year in paper_cum_citation_dict[paper] else (0, i) for i,paper in enumerate(paper_list)]
    citation_list.sort(reverse=True)
    ranklist = [0] * len(paper_list)
    rank = 0
    prevCits = float('inf')
    # print(citation_list)
    # exit(0)
    for data in citation_list:
        if data[0] < prevCits:
            rank += 1
        ranklist[data[1]] = rank
        prevCits = data[0]

    # print([(data[0], paper_list[data[1]], year, d_index_dict[data[1]]) for data in citation_list[:10]])
    return ranklist

def get_delta_citation_ranklist(paper_list, year1, year2, paper_cum_citation_dict, paper_year_dict, d_index_dict):
    # citation_list = []
    # for i,paper in enumerate(paper_list):
    #     if paper in paper_cum_citation_dict and year in paper_cum_citation_dict[paper]:
    #         print(paper_cum_citation_dict[paper])
    #         citation_list.append((paper_cum_citation_dict[paper][year], i))
    #     else:
    #         citation_list.append((0,i))

    # print(len([paper for paper in paper_list if paper in paper_cum_citation_dict]))
    # exit(0)
    citation_list = [((paper_cum_citation_dict[paper][year2] - paper_cum_citation_dict[paper][year1]) / float(1 + paper_cum_citation_dict[paper][year1]), i) if paper in paper_cum_citation_dict and year1 in paper_cum_citation_dict[paper] and year2 in paper_cum_citation_dict[paper] else (0, i) for i,paper in enumerate(paper_list)]
    citation_list.sort(reverse=True)
    ranklist = [0] * len(paper_list)
    rank = 0
    prevCits = float('inf')
    # print(citation_list)
    # exit(0)
    for data in citation_list:
        if data[0] < prevCits:
            rank += 1
        ranklist[data[1]] = rank
        prevCits = data[0]

    # print([(data[0], paper_list[data[1]], year, d_index_dict[data[1]]) for data in citation_list[:10]])
    return ranklist

def get_h_index_ranklist(paper_list, year, paper_branch_data, paper_year_dict):
    pass

def spearman_rank_correlation(ranklist1, ranklist2):
    rho, pval = spearmanr(ranklist1, ranklist2)
    return rho