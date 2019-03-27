from pathlib import Path
import json
from tools import read_dna
from tools import read_tform
import pandas as pd
from statistical_tools import get_knn_error

TEST_DIR = Path.cwd() / "TestData" / "knn_layer_swap_40"
LABELS_PATH = Path.cwd() / "RBMTrainingDataset" / "2018_labels_eos.csv"
LABELS = pd.read_csv(str(LABELS_PATH) , sep=',' , header=None).values

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



if __name__ == "__main__":
    knn_error_reports(TEST_DIR)
