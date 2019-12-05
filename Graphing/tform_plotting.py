# the basic functionality of plotting the tform produced by a trained neural network
import pandas as pd
from plotting_tools import position_color_dict
from plotly import __version__
from plotly.offline import download_plotlyjs , init_notebook_mode , iplot, plot
import plotly.graph_objs as go


#inputs
#   tform_data  : a dataframe of the tform to plot
#   labels_data : a dataframe of the labels corresponding to the tform
def plot_tform_2d(tform_data , labels_data , child_name):
    # ensure data is in correct format--pandas Data Frame
    assert type(tform_data) is pd.DataFrame , "tform_data is not a Data Frame"
    assert type(labels_data) is pd.DataFrame , "labels_data is not a Data Frame"

    # add a header to the data for convenience
    tform_columns = ["xaxis" , "yaxis"]
    tform_data.columns = tform_columns

    labels_columns = ["name" , "position" , "team"]
    labels_data.columns = labels_columns

    merged = pd.concat([tform_data , labels_data] , axis=1)
    #colours = merged['position'].map(position_color_dict)

    #create our figure for graphing
    fig = go.Figure()

    # separately graph all the positions
    for position in merged.position.unique():
        # isolate this position
        pos_df = merged[merged.position == position]
        fig.add_trace(go.Scatter(
            x = pos_df.xaxis ,
            y = pos_df.yaxis ,
            mode = 'markers' ,
            marker_color =  position_color_dict[position] ,
            text = pos_df.name ,
            name = position
        ))

    fig.update_layout(title=(child_name) , hovermode='closest')

    return fig

def plot_tform_3d(tform_data , labels_data , savename):
    # ensure data is in correct format--pandas Data Frame
    assert type(tform_data) is pd.DataFrame , "tform_data is not a Data Frame"
    assert type(labels_data) is pd.DataFrame , "labels_data is not a Data Frame"

    # add a header to the data for convenience
    tform_columns = ["xaxis" , "yaxis" , 'zaxis']
    tform_data.columns = tform_columns

    labels_columns = ["name" , "position" , "team"]
    labels_data.columns = labels_columns

    merged = pd.concat([tform_data , labels_data] , axis=1)
    #colours = merged['position'].map(position_color_dict)

    #create our figure for graphing
    fig = go.Figure()

    # separately graph all the positions
    for position in merged.position.unique():
        # isolate this position
        pos_df = merged[merged.position == position]
        fig.add_trace(go.Scatter3d(
            x = pos_df.xaxis ,
            y = pos_df.yaxis ,
            z = pos_df.zaxis ,
            mode = 'markers' ,
            marker_color =  position_color_dict[position] ,
            text = pos_df.name ,
            name = position
        ))

    fig.update_layout(title=(savename) , hovermode='closest')

    plot(fig , filename=(savename + ".html") , auto_open=False)



if __name__ == "__main__":
    tform_data = pd.read_csv("tform3d.csv" , sep=',' , header=None)
    labels_data = pd.read_csv("labels.csv" , sep=',' , header=None)
    plot_tform_3d(tform_data , labels_data , '3dtest')
