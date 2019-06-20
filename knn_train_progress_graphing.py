from plotly import __version__
from plotly import tools
from plotly.offline import download_plotlyjs , init_notebook_mode , iplot, plot
import plotly.graph_objs as go
from pathlib import Path
import pandas as pd

# universal color dict
pos_color_dict = {
    "QB":'rgb(21,97,219)',
    "RB":'rgb(34,216,128)',
    "WR":'rgb(226,92,24)',
    "0":'rgb(228,232,11)',
    "TE":'rgb(232,11,221)'
}

# universal labels file
labelsfile = Path.cwd() / "RBMTrainingDataset" / "2018_labels_eos.csv"
labels = pd.read_csv(str(labelsfile) , sep=',', header=None)

def get_performer_data(performer):
    gen_name = performer[1]
    child_name = performer[2]
    target_file = Path.cwd() / "TestData" / "knn_layer_swap_40" / gen_name / child_name / "tform.csv"
    data = pd.read_csv(str(target_file) , sep=',' , header=None)
    return data


def make_graph():
    # get ordered list of all the best performers in generation
    data_dir = Path.cwd() / "TestData" / "knn_layer_swap_40" / "BestPerformers"
    best_list = open(str(data_dir / "best_performers.txt") , 'r')
    best_performers = []
    for line in best_list:
        gen_name , child_name = line.split(':')
        child_name = child_name.strip(' ')
        _ , int_key = gen_name.split('_')
        best_performers.append((int(int_key) , gen_name , child_name.rstrip()))
    best_performers.sort(key=lambda x : x[0])
    # now have a list of tuples (int_key , generation_name , child_name)

    traces = []

    #for each child in the generation get data and create a trace
    for performer in best_performers:
        performer_data = get_performer_data(performer)
        # format data
        d = {'x':performer_data[0] , 'y':performer_data[1] , 'name':labels[0] , 'team':labels[2] , 'pos':labels[1]}
        merged = pd.DataFrame(data=d)
        cols = merged['pos'].map(pos_color_dict)

        # turn into trace
        trace = go.Scatter(
            x=merged['x'],
            y=merged['y'],
            mode='markers',
            marker=dict(color=cols),
            text=merged['name']
        )

        traces.append(trace)

    #list of all our names
    plot_names = []
    for performer in best_performers:
        plot_names.append(performer[1])

    # we now have a list of traces to append to fig
    fig = tools.make_subplots(rows=6, cols=5 , subplot_titles=plot_names)
    row = 1
    col = 1

    for trace in traces:
        fig.append_trace(trace , row , col)
        if col < 5:
            col = col + 1
        else:
            row = row + 1
            col = 1

    fig['layout'].update(height=2160, width=3840, title='i <3 annotations and subplots')
    plot(fig, filename='simple-subplot-with-annotations')




if __name__ == '__main__':
    make_graph()
