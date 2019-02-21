# various functions for visualization
import matplotlib.pyplot as plt
from pathlib import Path
from visualization_tools import pos_color_dict as label_dict
import pandas as pd
import numpy as np


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


def graph_model_training_loss(path_to_directory, save_dir, save_filename):
    # calculate curve of best fit
	csv_target = path_to_directory / 'loss.csv'
	csv = pd.read_csv(str(csv_target) , sep=',' , header=None)
	vals = csv.values[0]
	points = [(x,y) for x, y in enumerate(vals)]
	x = [x for x,y in points]
	y = [y for x,y in points]

	z = np.polyfit(x, y, 2)
	f = np.poly1d(z)
	f_prime = np.polyint(f)
	# we are always integrating from x[-1], the max x coordinate, to 0, so we only are concerned about the max value for def integral
	area_under_curve = f_prime(x[-1])

	x_new = np.linspace(x[0] , x[-1] , x[-1])
	y_new = f(x_new)


	# plot the datapoints and the curve of best fit on top of it
	plt.plot(x,y,'b.')
	plt.plot(x_new,y_new,'m-',linewidth=3)
	filename = save_dir / save_filename
	plt.savefig(str(filename))
	plt.clf()
