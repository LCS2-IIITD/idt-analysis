from sklearn.linear_model import LogisticRegression
from get_induced_graph import build_entire_graph, get_induced_tree, get_tree_features
import argparse
import pickle
import numpy as np
from sklearn.metrics import precision_score

parser = argparse.ArgumentParser()
parser.add_argument('--model_input', type=str)

args = parser.parse_args()

def normalise(v):
    v = (v - np.mean(v))/np.std(v)
    return v

def parse_input():
    with open(args.model_input) as f:
        a = f.readlines()
    data_matrix = []
    text = []
    with open(args.model_input) as f:
        text = f.readlines()
    text = [l.strip().split() for l in text]
    for line in text:
        data_matrix.append([float(l) for l in line[1:]])
    return np.array(data_matrix)

data_matrix = parse_input()

for i in range(data_matrix.shape[1] - 1):
    data_matrix[:,i] = normalise(data_matrix[:,i])

# print(data_matrix)

tot_data_matrix = data_matrix[:76,:]
nontot_data_matrix = data_matrix[76:,:]

np.random.shuffle(nontot_data_matrix)

avg_acc = []
model_coefs = []

nneg = 80

for i in range(0, nontot_data_matrix.shape[0], nneg):
    np.random.shuffle(tot_data_matrix)
    final_data_matrix = np.vstack((tot_data_matrix, nontot_data_matrix[i:i+nneg,:]))

    n, m = final_data_matrix.shape

    model = LogisticRegression()

    xtrain = final_data_matrix[:int(0.7*n), :(m-1)]
    ytrain = final_data_matrix[:int(0.7*n), m-1]
    xtest = final_data_matrix[int(0.7*n):, :(m-1)]
    ytest = final_data_matrix[int(0.7*n):, m-1]
    model.fit(xtrain, ytrain)
    avg_acc.append(model.score(xtest, ytest))
    print(avg_acc[-1])

    # print(model.coef_)
    model_coefs.append(model.coef_)

avg_acc = np.array(avg_acc)
model_coefs = np.array(model_coefs)

print('Avg accuracy: ', np.mean(avg_acc))
print('Stddev accuracy: ', np.std(avg_acc))

print('Avg model-coefs: ', np.mean(model_coefs, 0))
print('Stddev model-coefs: ', np.std(model_coefs, 0))

# step = n // 5
# acc = 0
# for i in range(5):
#     ibegin = i*step
#     iend = (i+1)*step
#     # print(ibegin, iend)
#     # print(data_matrix[:ibegin, :m-1])
#     # print(data_matrix[iend:, :m-1])
#     if ibegin == 0:
#         trainX = data_matrix[iend:, :m-1]
#         trainY = data_matrix[iend:,m-1]
#     else:
#         trainX = np.vstack((data_matrix[:ibegin, :m-1],data_matrix[iend:, :m-1]))
#         # print(data_matrix[:ibegin, m-1])
#         # print(data_matrix[iend:, m-1])
#         trainY = np.hstack((data_matrix[:ibegin, m-1],data_matrix[iend:, m-1]))
    
#     testX = data_matrix[ibegin:iend, :m-1]
#     testY = data_matrix[ibegin:iend, m-1]

#     model = LogisticRegression()
#     model.fit(trainX, trainY)
#     acc += model.score(testX, testY)

# print('Accuracy: ', acc/5.0)
