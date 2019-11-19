# imports
from pathlib import Path
import pandas as pd
import numpy as np
import json


# method that returns the euclidian dist between two points
def get_euclidian_dist(point_1 , point_2 , data_dim):
    distance = 0
    for x in range(data_dim):
        distance += np.square(point_1[x] - point_2[x])
    return np.sqrt(distance)

def knn(tform , labels):
