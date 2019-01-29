from plotly import __version__
from plotly.offline import download_plotlyjs , init_notebook_mode , iplot, plot
import plotly.graph_objs as go
from pathlib import Path
import pandas as pd
from tools import get_ndarray


testfile = Path.cwd() / "40test.csv"
labelsfile = Path.cwd() / "RBMTrainingDataset" / "2018_labels.csv"


#data = get_ndarray(testfile)
data = pd.read_csv(str(testfile) , sep=',' , header=None)
labels = pd.read_csv(str(labelsfile) , sep=',', header=None)
l = []

'''
for name, team, pos in [(name,team,pos) for name,team,pos in labels]:
    l.append([name,team,pos])
'''



pos_color_dict = {
    "QB":'rgb(21,97,219)',
    "RB":'rgb(34,216,128)',
    "WR":'rgb(226,92,24)',
    "0":'rgb(228,232,11)',
    "TE":'rgb(232,11,221)'
}


d = {'x':data[0] , 'y':data[1] , 'name':labels[0] , 'team':labels[1] , 'pos':labels[2]}
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
plot(data, filename="test.html")
