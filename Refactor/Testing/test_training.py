# file testing behavior of our Genetics class
from pathlib import Path
import sys
parent_dir = str(Path.cwd().parent)
sys.path.append(parent_dir)

import run_test
import pandas as pd

test_name = "RefactoredTest3"
num_gen = 2
gen_size = 4

# get the datas

train_data_name = "training_set.csv"
train_data_path = Path.cwd().parent.parent / "RBMTrainingDataset" / train_data_name
train_data = pd.read_csv(str(train_data_path) , sep=',' , header=None).values

test_data_name = "2018_data_eos.csv"
test_data_path = Path.cwd().parent.parent / "RBMTrainingDataset" / test_data_name
test_data = pd.read_csv(str(test_data_path) , sep=',' , header=None).values

labels_data_name = "2018_labels_eos.csv"
labels_data_path = Path.cwd().parent.parent / "RBMTrainingDataset" / labels_data_name
labels_data = pd.read_csv(str(labels_data_path) , sep=',' , header=None).values

output_dim = 2
eval_type = "knn_error"

write_directory = Path.cwd() / "TrainingTestFolder"


run_test.train(test_name , num_gen, gen_size, train_data , train_data_name , test_data , test_data_name , labels_data , labels_data_name , output_dim, eval_type, write_directory)
