# Python script containing functions for loading tranined model, getting
# a transformation on test data from trained model

from pathlib import Path
from core import Parametric_tSNE
from tools import write_csv
from tools import get_ndarray
import visualization as vis

# load model given a direct path to it, and returns a transformation of specified test data as an ndarray
def load_and_transform(path_to_model , test_data, num_perplexities, output_dims):
    '''
        path_to_model: a python pathlib path to the model to be loaded
        test_data: data that has already been loaded and formatted to an np array (i.e. the df.values)
        num_perplexities: the number of perplexities originally used to train the model
        output_dims: the original output dimensionality of the model

        returns: numpy.ndarray of the transformed data
    '''
    # grab the dimensionality of the numpy ndarray
    input_dims = len(test_data[0])

    # instance a ptsne object of this dimensionality and restore model
    ptsne = Parametric_tSNE(input_dims , output_dims , num_perplexities)
    ptsne.restore_model(str(path_to_model) , num_perplexities=num_perplexities)

    # get transformation
    transform = ptsne.transform(test_data)

    return transform

# model_evaluation loads up a trained model and a test dataset and writes a csv of the transformed data
def model_evaluation(path_to_model_dir, path_to_data_file, save_path, save_name, output_dims=2):
    # load data
    test_data = get_ndarray(path_to_data_file)
    # load perplexities
    perp = int((path_to_model_dir / "perplexity.txt").read_text())
    # get transform
    transform = load_and_transform((path_to_model_dir / "model") , test_data , perp, output_dims)
    # write it out
    write_csv(transform , (save_path / save_name))

# produce and show a graph of a transformed dataset
def show_transformation_graph(path_to_data , path_to_labels, seg="position"):
    data = get_ndarray(path_to_data)
    labels = get_ndarray(path_to_labels)

    if seg is "position":
        vis.graph_transformation_positions(data, labels)

# save a graph of transformed dataset
def save_transformation_graph(path_to_data , path_to_labels , save_dir , save_name , seg="position"):
    data = get_ndarray(path_to_data)
    labels = get_ndarray(path_to_labels)

    if seg is "position":
        vis.save_transformation_graph(data, labels , save_dir, save_name)
