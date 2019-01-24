import pickle

paper_year_dict = {}
with open('./data/PAPER_YEAR_DICT.pickle', 'rb') as f:
    paper_year_dict = pickle.load(f)

paper_conference_dict = {}
with open('./data/PAPER_VENUE_DICT_CONF.pickle', 'rb') as f:
    paper_conference_dict = pickle.load(f)

TOTpaper_venue_dict = {}
with open('./data/YEAR_VENUE_OF_AWARD_DICT.pickle', 'rb') as f:
    TOTpaper_venue_dict = pickle.load(f)

conf_paper_list_dict = {}

for paper,venue in paper_conference_dict.items():
    if paper in paper_year_dict:
        year = paper_year_dict[paper]
        # print(year)
        if venue not in conf_paper_list_dict:
            conf_paper_list_dict[venue] = {}
        if year not in conf_paper_list_dict[venue]:
            conf_paper_list_dict[venue][year] = []
        conf_paper_list_dict[venue][year].append(paper)

with open('./data/CONF_PAPERS_DICT2.pkl', 'wb') as f:
    pickle.dump(conf_paper_list_dict, f)
