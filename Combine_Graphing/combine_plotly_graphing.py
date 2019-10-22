from plotly import __version__
from plotly.offline import download_plotlyjs , init_notebook_mode , iplot, plot
import plotly.graph_objs as go
from pathlib import Path
import pandas as pd



labelsfile = Path.cwd().parent / "NFL_Combine_Data" / "2019Both.csv"

def plot_and_save(input_folder):

    testfile = input_folder / "tform.csv"
    #data = get_ndarray(testfile)
    data = pd.read_csv(str(testfile) , sep=',' , header=None)
    labels = pd.read_csv(str(labelsfile) , sep=',', header=0)
    l = []

    '''
    pos_color_dict = {
        "1st":'rgb(21,97,219)',
        "2nd":'rgb(34,216,128)',
        "3rd":'rgb(226,92,24)',
        "4th":'rgb(228,232,11)',
        "5th":'rgb(232,11,221)',
        "6th":'rgb(232, 39, 226)',
        "7th": 'rgb(50, 240, 17)' ,
        "undrafted":'rgb(0,0,0)'
    }
    '''

    pos_color_dict = {
        "S" : 'rgb(7, 242, 70)' , # def GREEN
        "OT" : 'rgb(0, 68, 255)' , # off BLUE
        "LT" : 'rgb(0, 68, 255)' , # lineman
        "EDGE" : 'rgb(7, 242, 70)' , #lineman
        "DL" : 'rgb(7, 242, 70)' , #lineman
        "RB" : 'rgb(0, 68, 255)' , # skill
        "WR" : 'rgb(0, 68, 255)' , # skill
        "CB" : 'rgb(7, 242, 70)' , # skill
        "P" : 'rgb(158, 7, 240)' , # special PURPLE
        "OL" : 'rgb(0, 68, 255)' , # lineman
        "TE" : 'rgb(0, 68, 255)' , # tight end ORANGE
        "QB" : 'rgb(240, 7, 27)' , # quarterback RED
        "K" : 'rgb(0, 68, 255)' , # special
        "LS" : 'rgb(7, 242, 70)' , # skill
        "FB" : 'rgb(0, 68, 255)' # skill
    }


    #d = {'x':data[0] , 'y':data[1] , 'name':labels["Player"].apply(lambda x : x.split('\\')[0]) , 'drafted': labels['Drafted (tm/rnd/yr)'].apply(lambda x : x.split('/')[1].strip() if type(x) is str else 'undrafted')}
    d = {'x':data[0] , 'y':data[1] , 'name':labels["Player"].apply(lambda x : x.split('\\')[0]) , 'pos': labels['Pos']}
    merged = pd.DataFrame(data=d)

    cols = merged['pos'].map(pos_color_dict)

    trace0 = go.Scatter(
        x=merged['x'],
        y=merged['y'],
        mode='markers',
        marker=dict(color=cols),
        text=merged['name']
    )

    # not sure how this layout stuff works?
    layout = go.Layout(
        title="Network Tranformation of 2018 players",
        hovermode='closest'
    )

    data = [trace0]
    plot(data, filename=str(input_folder / "off_def_tform_plot.html") , auto_open=False)


def mass_plot(test_dir):
    # iterate through every generation subfolder
    for gen_dir in [x for x in test_dir.iterdir() if x.is_dir()]:
        for child_dir in [y for y in gen_dir.iterdir() if y.is_dir()]:
            plot_and_save(child_dir)


if __name__ == "__main__":
    mass_plot((Path.cwd() / "TestData" / "knn_layer_swap_40_fantasy_top_100"))
