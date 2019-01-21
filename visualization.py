# various functions for visualization
import matplotlib.pyplot as plt
from pathlib import Path
from visualization_tools import pos_color_dict as label_dict


# Note - some of the below functions are inherently dependent on the nature of the data
#       used in training/testing (specifically here NFL player statistics). As such,
#       these graphing functions would make little sense for other datasets, and other
#       visualaztion techniques should be developed for other datasets

# plots the results by position and displays to screen
def graph_transformation_positions(data_ndarray , labels_ndarray):
    merged_list = get_plotlist(data_ndarray , labels_ndarray)

    for (x,y,name,team,pos) in merged_list:
        plt.plot(x, y, label_dict[pos])

    plt.show()
    plt.clf()

# plots the results by position and saves the graph as pdf located as specified position
def save_transformation_graph(data_ndarray , labels_ndarray, save_path, save_name):
    merged_list = get_plotlist(data_ndarray , labels_ndarray)

    for (x,y,name,team,pos) in merged_list:
        plt.plot(x,y,label_dict[pos])

    plt.savefig(str(save_path / save_name))
    plt.clf()


# gets ndarray of data and player labels and returns a merged list for ease of plotting
# returns list of tuples of form (xcoord, ycoord, name, team, position)
def get_plotlist(data_ndarray , labels_ndarray):
    x_vals = [x for x,y in data_ndarray]
    y_vals = [y for x,y in data_ndarray]
    labels = [(name,team,pos) for name,team,pos in labels_ndarray]

    merged_list = []
    for x,y, (name,team,pos) in zip(x_vals , y_vals , labels):
        merged_list.append((x,y,name,team,pos))

    return merged_list

# TODO
def graph_transformation_fantasy_perf(data_ndarray, labels_ndarray):
    pass
