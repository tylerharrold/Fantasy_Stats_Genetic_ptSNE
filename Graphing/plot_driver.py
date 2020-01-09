# a driver with functions designed to batch plot
from pathlib import Path
import json
import pandas as pd
from tform_plotting import plot_tform_2d
from tform_plotting import plot_tform_3d
from tform_plotting import plot_tform_2d_combine , plot_tform_3d_combine
from plotly import __version__
from plotly.offline import download_plotlyjs , init_notebook_mode , iplot, plot
import plotly.graph_objs as go


# iterates through the best performers of a generation and plots their tform, saving results to specified folder
def plot_best_performers(test_dir , save_folder, plot_func , label_path , label_header=None):

    label_data = pd.read_csv(str(label_path) , sep=',' , header=label_header)
    for generation in [folder for folder in test_dir.iterdir() if folder.is_dir()]:
        with open(str(generation / "half_auc_error_report.json") , 'r') as json_file:
            half_auc_data = json.load(json_file)
        child_name , _ = get_best_performers_training(half_auc_data)
        #get the data
        test_data = pd.read_csv(str(generation / child_name / 'tform.csv') , sep=',' , header=None)
        fig = plot_func(test_data , label_data , child_name)
        savename = generation.name + "_" + child_name + '.html'
        plot(fig , filename=str(save_folder / savename) , auto_open=False)



# plots the tform of each member of a generation
def plot_test_generation():
    pass

# plot the tforms of an entire test
def plot_test():
    pass

# plot the training curves of the best performers
def plot_training_curve():
    pass

# based on the json report in a generation, returns the name of the best performer, using its training performance
def get_best_performers_training(data_dict):
    # the best training performer is the one with the lowest half_auc_value
    lowest_to_highest = sorted(data_dict.items() , key=lambda x : x[1]['loss'])
    return lowest_to_highest[0]

# based on the json report in a generation, returns the name of the best performer, using the post training knn eval of the tform
def get_best_performers_knn():
    pass

def test_integrity(test_dir):
    for generation in [folder for folder in test_dir.iterdir() if folder.is_dir()]:
        with open(str(generation / "half_auc_error_report.json") , 'r') as json_file:
            half_auc_data = json.load(json_file)
        child_name , _ = get_best_performers_training(half_auc_data)
        print(generation.name + 's best performer was ' + child_name)

if __name__ == "__main__":
    #test_dir = Path.cwd().parent / "TestData" / "normalized_fantasy_30_40_half_auc"
    #save_folder = Path.cwd().parent / "TestData" / "Graphs" / "Norm_Fant_2d_Evolved"
    #plot_func = plot_tform_2d
    fantasy_label_path = Path.cwd().parent / "RBMTrainingDataset" / "2018_labels_eos.csv"
    combine_label_path = Path.cwd().parent / "NFL_Combine_Data" / "2019Both.csv"
    fantasy_label_header = None
    combine_label_header = 0
    #label_header = None
    #plot_best_performers(test_dir , save_folder ,  plot_func , label_path , label_header)


    tests_to_graph = [
		[Path.cwd().parent / "TestData" / "normalized_combine_flat_40_half_auc" , Path.cwd().parent / "TestData" / "Graphs" / "Norm_Comb_2d_Flat" , plot_tform_2d_combine , combine_label_path , combine_label_header] ,
		[Path.cwd().parent / "TestData" / "normalized_combine_30_40_half_auc" , Path.cwd().parent / "TestData" / "Graphs" / "Norm_Comb_2d_Evolved" ,  plot_tform_2d_combine , combine_label_path , combine_label_header] ,
		[Path.cwd().parent / "TestData" / "normalized_combine_3D_flat_40" , Path.cwd().parent / "TestData" / "Graphs" / "Norm_Comb_3d_Flat" , plot_tform_3d_combine , combine_label_path , combine_label_header] ,
		[Path.cwd().parent / "TestData" / "normalized_combine_3D_30_40_half_auc" , Path.cwd().parent / "TestData" / "Graphs" / "Norm_Comb_3d_Evolved" , plot_tform_3d_combine , combine_label_path , combine_label_header] ,
		[Path.cwd().parent / "TestData" / "hyper_mutate_normalized_combine_3D_30_40_half_auc" , Path.cwd().parent / "TestData" / "Graphs" / "Norm_Comb_3d_Hyper_Evolved" , plot_tform_3d_combine , combine_label_path , combine_label_header] ,
		[Path.cwd().parent / "TestData" / "normalized_fantasy_flat_40_half_auc" , Path.cwd().parent / "TestData" / "Graphs" / "Norm_Fant_2d_Flat" , plot_tform_2d , fantasy_label_path , fantasy_label_header] ,
		[Path.cwd().parent / "TestData" / "normalized_fantasy_3D_flat_40_half_auc" , Path.cwd().parent / "TestData" / "Graphs" / "Norm_Fant_3d_Flat" , plot_tform_3d , fantasy_label_path , fantasy_label_header] ,
		[Path.cwd().parent / "TestData" / "normalized_fantasy_3D_30_40_half_auc", Path.cwd().parent / "TestData" / "Graphs" / "Norm_Fant_3d_Evolved" , plot_tform_3d , fantasy_label_path , fantasy_label_header]
	]

    for test_dir , save_folder_path , plot_func , label_path, label_header in tests_to_graph:
        save_folder_path.mkdir()
        plot_best_performers(test_dir , save_folder_path , plot_func , label_path , label_header)

    '''
    testdir = Path.cwd().parent / "TestData" / "normalized_fantasy_30_40_half_auc"
    test_integrity(testdir)
    '''
    '''
    testdir = Path.cwd().parent / "TestData" / "normalized_fantasy_30_40_half_auc"
    savedir = Path.cwd() / "best_plots_question_mark"
    graph_func = plot_tform_2d
    labelpath = Path.cwd() / "labels.csv"
    plot_best_performers(testdir , savedir , graph_func , labelpath)
    '''
