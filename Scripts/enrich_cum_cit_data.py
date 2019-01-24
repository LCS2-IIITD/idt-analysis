import pickle

pyd = {}
with open('./data/PAPER_YEAR_DICT.pickle', 'rb') as f:
    pyd = pickle.load(f)

pccd = {}
with open('./data/CUMMULATIVE_CITATIONS.pickle', 'rb') as f:
    pccd = pickle.load(f)

pccd_new = pccd.copy()

for paper, cum_cit in pccd_new.items():
    pubYear = pyd[paper]
    # print(pubYear)
    if int(pubYear) not in cum_cit:
        pccd_new[paper][int(pubYear)] = 0
        # print('no first')
    for year in range(int(pubYear) + 1, 2011):
        if year not in cum_cit:
            pccd_new[paper][year] = pccd_new[paper][year - 1]

with open('./data/CUMMULATIVE_CITATIONS_ENRICHED.pickle', 'wb') as f:
    pickle.dump(pccd_new, f)