# evaluates the errors of our trained transforms using a knn (where k=1) algorithm
# created with ispiration by https://www.analyticsvidhya.com/blog/2018/03/introduction-k-neighbours-algorithm-clustering/

# imports
from pathlib import Path
import pandas as pd
import numpy as np

# functions

# method that returns the euclidian dist between two points
def get_euclidian_dist(point_1 , point_2 , data_dim=2):
    distance = 0
    for x in range(data_dim):
        distance += np.square(point_1[x] - point_2[x])
    return np.sqrt(distance)


# script

# constants
TRANSFORM_TGT = Path.cwd() / "Flat40vTrained40" / "best_of_trained_tform.csv"
LABELS = Path.cwd() / "RBMTrainingDataset" / "2018_labels_eos.csv"

# load our data
tform = pd.read_csv(str(TRANSFORM_TGT) , sep=',' , header=None).values
labels = pd.read_csv(str(LABELS) , sep=',' , header=None).values



dist_table = []

#create a table of distances for each point
assert(len(tform) == len(labels))
for i in range(len(tform)):
    row = []
    for j in range(len(tform)):
        if i==j:
            row.append(None)
        else:
            row.append(get_euclidian_dist(tform[i] , tform[j]))
    dist_table.append(row)

# iterate through each row, identifying the nearest neighbor and using that to get its classification
accuracy_table = []

for j in range(len(dist_table)):
    lowest_index = -1
    for i in range(len(dist_table[j])):
        if dist_table[j][i] is not None:
            dist = dist_table[j][i]
            if lowest_index < 0:
                lowest_index = i
            else:
                if dist < dist_table[j][lowest_index]:
                    lowest_index = i
    pred_v_true = []
    pred_v_true.append(labels[j][0])
    pred_v_true.append(labels[lowest_index][1])
    pred_v_true.append(labels[j][1])
    accuracy_table.append(pred_v_true)

errors = 0
for i in accuracy_table:
    if i[1] is not i[2]:
        print(i)
        errors = errors + 1

num = len(accuracy_table)

error_pctg = errors / num
print("The error rate was:" , error_pctg)
