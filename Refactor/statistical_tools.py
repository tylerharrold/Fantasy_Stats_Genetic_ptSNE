import pandas as pd
import numpy as np
import json

# get the knn error percentage
# created with ispiration by https://www.analyticsvidhya.com/blog/2018/03/introduction-k-neighbours-algorithm-clustering/
def _get_euclidian_dist(point_1 , point_2 , data_dim):
    distance = 0
    for x in range(data_dim):
        distance += np.square(point_1[x] - point_2[x])
    return np.sqrt(distance)

def get_knn_error(tform , labels):
    dist_table = []

    data_dim = len(tform[0])

    assert(len(labels) == len(tform))

    for i in range(len(tform)):
        row = []
        for j in range(len(tform)):
            if i == j:
                row.append(None)
            else:
                row.append(_get_euclidian_dist(tform[i] , tform[j] , data_dim))
        dist_table.append(row)

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
        pred_v_true.append(labels[j])
        pred_v_true.append(labels[lowest_index])
        accuracy_table.append(pred_v_true)

    errors = 0
    for i in accuracy_table:
        if i[0][1] is not i[1][1]:
            errors = errors + 1
    num = len(accuracy_table)
    error_pctg = errors / num
    return error_pctg
