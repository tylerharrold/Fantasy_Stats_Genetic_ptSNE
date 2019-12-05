# train a parametric t-SNE network using the 'standard' shape used by Van der Maaten in his paper
from pathlib import Path
import os
from core import Parametric_tSNE
from tools import get_ndarray
from tools import write_loss
from tools import write_csv
from tools import get_area_under_half_curve
import json
from knn_reporting import avg_knn_error
import pandas as pd

def run_standard_ptsne(test_name_path , train_data_path , test_data_path , output_dims=2):
    # create a folder with the test_name
    os.mkdir(str(test_name_path))

    # get relevant data
    raw_data = get_ndarray(train_data_path)
    test_data = get_ndarray(test_data_path)
    input_dims = len(raw_data[0])
    perplexity = 30

    ptsne = Parametric_tSNE(input_dims, output_dims, perplexity)
    loss = ptsne.fit(raw_data , verbose=False)
    tform = ptsne.transform(test_data)

    # write out data
    write_loss(test_name_path , loss)
    write_csv(tform , (test_name_path / "tform.csv"))

    ptsne.clear_session()

def write_reports(test_folder , labels_path , labels_identifying_col=1):
    # retrieve our loss
    loss_csv = test_folder / 'loss.csv'
    losses = pd.read_csv(str(loss_csv) , sep=',' , header=None)
    half_auc_error = get_area_under_half_curve(losses)
    name = "vdm_standard"
    data = {}
    data[name] = {'loss':half_auc_error}
    with open(str(test_folder / "avg_loss.json") , 'w') as json_file:
        json.dump(data, json_file)

    labels = pd.read_csv(str(labels_path) , sep=',' , header = None).values
    tform_path = test_folder / "tform.csv"
    tform = pd.read_csv(str(tform_path) , sep=',' , header=None).values
    knn_error = avg_knn_error(tform , labels , labels_identifying_col)
    data={}
    data[name] = {'knn_error':knn_error}
    with open(str(test_folder / 'knn_error.json') , 'w') as json_file:
        json.dump(data , json_file)

if __name__ == "__main__":
    test_name_path = Path.cwd() / "TestData" / "VDM_Standard_2d_fantasy_normalized"
    train_data_path = Path.cwd() / "Normalized_Fantasy_Data" / "normalized_training_set.csv"
    test_data_path = Path.cwd() / "Normalized_Fantasy_Data" / "normalized_test_set.csv"
    output_dims = 2
    #run_standard_ptsne(test_name_path , train_data_path , test_data_path , output_dims)

    labels_path = Path.cwd() / "RBMTrainingDataset" / "2018_labels_eos.csv"
    labels_identifying_col = 1
    write_reports(test_name_path , labels_path , labels_identifying_col)
