from pathlib import Path
import json
from tools import read_dna
from tools import read_tform
import pandas as pd
from statistical_tools import get_knn_error
import math

TEST_DIR = Path.cwd() / "TestData" / "knn_layer_swap_40"
LABELS_PATH = Path.cwd() / "RBMTrainingDataset" / "2018_labels_eos.csv"
LABELS = pd.read_csv(str(LABELS_PATH) , sep=',' , header=None).values

CONTROL_GROUP = Path.cwd() / "TestData" / "knn_layer_swap_flat_40" / "generation_1"
TEST_GROUP = Path.cwd() / "TestData" / "knn_layer_swap_40" / "generation_30"

# for each generation, prints a report containing children's names, knn_errors, and dna
def knn_error_reports(test_dir):
    # iterate through every generation subfolder
    for gen_dir in [x for x in test_dir.iterdir() if x.is_dir()]:
        # create a dict to turn into a generational stat report
        data = {}
        for child_dir in [y for y in gen_dir.iterdir() if y.is_dir()]:
            dna = read_dna(child_dir)
            tform = read_tform(child_dir)
            knn_error = get_knn_error(tform , LABELS)
            name = child_dir.name
            data[name] = {'knn_error':knn_error , 'dna' : dna}
        with open(str(gen_dir / "knn_error_report.json") , 'w') as json_file:
            json.dump(data , json_file)


# prints a json report of the mean, median and mode of the generation
def gen_stats_knn(test_dir):
    # iterate through every generation subfolder in a test
    for gen_dir in [x for x in test_dir.iterdir() if x.is_dir()]:
        # pull json
        with open(str(gen_dir / "knn_error_report.json") , 'r') as json_file:
            gen_data = json.load(json_file)
        total_knn = 0
        for i in gen_data:
            total_knn = total_knn + gen_data[i]['knn_error']
        mean = total_knn / len(gen_data)
        sum = 0
        for i in gen_data:
            sum = sum + (gen_data[i]['knn_error'] - mean)**2
        varience = sum / (len(gen_data) - 1)
        std_dev = math.sqrt(varience)
        n = len(gen_data)
        stat_data = {'mean' : mean , 'var' : varience , 'std_dev' : std_dev , 'n' : n}
        with open(str(gen_dir / "stat_report.json") , 'w') as outfile:
            json.dump(stat_data , outfile)

def t_test(gen_dir_1 , gen_dir_2):
    # load our stats
    with open(str(gen_dir_1 / "stat_report.json") , 'r') as infile:
        data1 = json.load(infile)

    with open(str(gen_dir_2 / "stat_report.json") , 'r') as infile:
        data2 = json.load(infile)

    df = data1['n'] + data2['n'] - 2


    t = (data1['mean'] - data2['mean']) / math.sqrt( (data1['var'] / data1['n']) + (data2['var'] / data2['n']))

    print(t)
    print(df)



if __name__ == "__main__":
    t_test(CONTROL_GROUP , TEST_GROUP)
