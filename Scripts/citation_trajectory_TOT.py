import pickle

er = None
with open('./data/citation_trajectory_categorisation_CS_Citation_Network/er_papers') as f:
    er = f.readlines()
er = set([int(l.strip()) for l in er[:-1]])

lr = None
with open('./data/citation_trajectory_categorisation_CS_Citation_Network/lr_papers') as f:
    lr = f.readlines()
lr = set([int(l.strip()) for l in lr[:-1]])

fr = None
with open('./data/citation_trajectory_categorisation_CS_Citation_Network/fr_papers') as f:
    fr = f.readlines()
fr = set([int(l.strip()) for l in fr[:-1]])

sr = None
with open('./data/citation_trajectory_categorisation_CS_Citation_Network/sr_papers') as f:
    sr = f.readlines()
sr = set([int(l.strip()) for l in sr[:-1]])

oth = None
with open('./data/citation_trajectory_categorisation_CS_Citation_Network/oth_papers') as f:
    oth = f.readlines()
oth = set([int(l.strip()) for l in oth[:-1]])

tot = None
with open('./data/matchedTOT_index_name_dict.pkl', 'rb') as f:
    tot = pickle.load(f)
tot = set([k for k,v in tot.items()])

tot_cat =  tot.intersection(er.union(fr).union(lr).union(sr).union(oth))
print('TOT papers categorised: ', len(tot_cat))

print('ER: ', 100*len(tot.intersection(er))/len(tot_cat))
print('LR: ', 100*len(tot.intersection(lr))/len(tot_cat))
print('FR: ', 100*len(tot.intersection(fr))/len(tot_cat))
print('SR: ', 100*len(tot.intersection(sr))/len(tot_cat))
print('OTH: ', 100*len(tot.intersection(oth))/len(tot_cat))
