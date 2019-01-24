import pickle
import csv

name_index_dict = dict()
index_name_dict = dict()

def DistJaccard(str1, str2):
	str1 = set(str1.lower().split())
	str2 = set(str2.lower().split())
	return float(len(str1 & str2)) / len(str1 | str2)

with open('./data/name_index_dict.pkl', 'rb') as f:
	name_index_dict = pickle.load(f, encoding='latin1')
	
with open('./data/index_name_dict.pkl', 'rb') as f:
	index_name_dict = pickle.load(f, encoding='latin1')

match_index_name_dict = dict()

csv_reader = None
with open('./data/TestOfTimeAwards.csv', 'rt') as f:
	csv_reader = csv.reader(f, delimiter=',', quotechar='"')

	i = 0
	for row in csv_reader:
		i += 1
		if i == 1:
			continue
		for paper,index in name_index_dict.items():
			if DistJaccard(paper, row[0]) >= 0.8:
				match_index_name_dict[index] = {'collected':row[0], 'dataset':paper}
				print(row[0])

with open('./data/matchedTOT_index_name_dict.pkl', 'wb') as f:
	pickle.dump(match_index_name_dict, f)
