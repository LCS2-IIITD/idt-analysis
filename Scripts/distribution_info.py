import networkx as nx 
import pickle
import random 
import collections
import operator
import sys
import matplotlib
import numpy as np 
from mpl_toolkits.mplot3d import Axes3D
from math import log10
from collections import OrderedDict
from scipy import stats 
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
BREADTH = 0
DEPTH = 1
TOTAL_CITATIONS = 2

def get_pickle_dump(filename):
	with open('./dumps/'+filename+'.pickle','rb') as handle:
		Variable = pickle.load(handle)
	return Variable

def dump_file(filename, Variable):
	with open('./dumps/'+filename+'.pickle','wb') as handle:
		pickle.dump(Variable,handle,protocol=pickle.HIGHEST_PROTOCOL)

data = get_pickle_dump("global_depth_breadth_v2")
# print(data)
depth_distribution = {}
breadth_distribution = {}

print("PAPER ID - BREADTH")




def normal_depth_breadth_plot(data):
	x = []
	y = []
	for w in data.keys():
		if data[w][TOTAL_CITATIONS] > 10:
			x.append(data[w][BREADTH]) #x axis is for breadth
			y.append(data[w][DEPTH]) #y axis is for depth
	plt.scatter(x , y)
	plt.xlabel("Breadth")
	plt.ylabel("Depth")
	plt.title("Depth Vs Breadth Plot")
	plt.savefig("Depth Vs Breadth_10.jpeg")
	plt.close()


def depth_vs_total_citation_given(data):
	x = []
	y = []
	for w in data.keys():
		# if data[w][TOTAL_CITATIONS] <= 2000:
		x.append(data[w][TOTAL_CITATIONS])
		y.append(data[w][DEPTH])
	plt.scatter(x,y)
	plt.xlabel("Total Citations")
	plt.ylabel("Depth")
	plt.title("Depth Vs Total Citations")
	plt.savefig("Depth Vs Total Citations.jpeg")
	plt.show() 
	# plt.close()
	
def breadth_vs_total_citation_given(data):
	x = []
	y = []
	for w in data.keys():
		# print(w) 
		x.append(data[w][TOTAL_CITATIONS])
		y.append(data[w][BREADTH])	

	plt.scatter(x,y)
	plt.xlabel("Total Citations")
	plt.ylabel("Breadth")
	plt.title("Breadth Vs Total Citations")
	plt.savefig("Breadth Vs Total Citations.jpeg")
	plt.show()
	# plt.close()

def plot_dict(new_distri_dict):
	plt.bar(range(len(new_distri_dict)) , list(new_distri_dict.values()))
	plt.xticks([0 , len(new_distri_dict) - 1] ,[round(min(list(new_distri_dict.keys())) , 2) , round(max(list(new_distri_dict.keys())) , 2) ] )  
	plt.xlabel('log10(No. Of Citations)')
	plt.ylabel('log10(Number Of Papers)')
	plt.title('Log Distribution Of Citations') 
	plt.show()

def citation_distribution(data):
	
	cit_count = [int(data[w][TOTAL_CITATIONS]) for w in data] 
	cit_count = collections.Counter(cit_count) 
	del cit_count[0] 
	
	prev=0 
	ordered_count = [k for k in list(cit_count.keys())]
	ordered_count.sort() 
	print(ordered_count)
	# for w in ordered_count:
	# 	print(w , cit_count[w] )
	for w in ordered_count:
		# print(w)
		cit_count[w] = cit_count[w] + prev 
		prev = cit_count[w] 

	new_distri_dict = {} 
	for w , k in cit_count.items():
		if w > 0:
			new_distri_dict[w] = log10(k)
	plot_dict(new_distri_dict)
	
	# plot_dict(cit_count)
	# citation_dict = [int(k) for k in data] 
	# num_eg =  [data[k] for k in data]
	# index = np.arange(max(citation_count)) 
	# counts = np.zeros(shape=len(index)) 
	# for i in citation_count:
	# 	print(i) 
	# 	counts[i-1] = new_distri_count.get(str(i), 0) 
 
	# plt.bar(index , counts , width = 0.4)

	# plt.savefig('Distribution (Cumulative).png') 




def scipy_plot(ordered_list):
	res = stats.cumfreq(ordered_list , numbins = 20) 
	print(res.cumcount) 


def td_scatter_plot(data):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	x = []
	y = []
	z = []
	for w in data.keys():
		if data[w][BREADTH] <= 1000:
			z.append(data[w][TOTAL_CITATIONS])
			x.append(data[w][BREADTH])
			y.append(data[w][DEPTH])
	# z = [data[w][TOTAL_CITATIONS] for w in data.keys()]
	# x = [data[w][BREADTH] for w in data.keys()]
	# y = [data[w][DEPTH] for w in data.keys()]
	ax.scatter(x , y, z)
	ax.set_xlabel("breadth")
	ax.set_ylabel("depth")
	ax.set_zlabel("total citations")
	plt.title("Depth Vs Breadth Vs Total Citations")
	plt.savefig("DEPTH VS BREADTH VS TOTAL CITATIONS.jpeg")
	plt.close()



breadth_vs_total_citation_given(data)
