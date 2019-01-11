import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
# need a function to write out the transformed data to a csv
# NOTE this function should be altered to write datafile into a specific directory
def write_csv(input_data, specified_filename):

	# turn input_data into a pandas dataframe
	df = pd.DataFrame(input_data)

	# write it out
	df.to_csv(path_or_buf=specified_filename , sep=',' , index=False, header=None)

# function that writes to a file called test_specs at the target location
# the 'shape' of a ptsne test, in bytes
# path parameter must be a Path object
def write_test_specs(path , num_gens , gensize):
	path = path / 'test_specs'
	path.write_bytes(bytes([num_gens,gensize]))

# writes dna, as text, to directory located at path
def write_dna(directory, dna):
	path = directory / 'dna.dna'
	path.write_text(dna)

# writes the area under curve of best fit
def write_auc(directory, auc):
	path = directory / 'auc.txt'
	path.write_text(str(auc))

# write loss data in specified directory in csv
def write_loss(directory, loss):
	path = directory / 'loss.csv'
	path.write_text(str(loss).strip('[]'))

# reads loss from folder path and returns list
# Note, needs fixing
def read_loss(directory):
	path = directory / 'loss.csv'
	return list(path.read_text())

def write_perplexity(directory, perplexity):
	path = directory / 'perplexity.txt'
	path.write_text(str(perplexity))

def write_shape(directory, shape):
	path = directory / 'shape.txt'
	path.write_text(str(shape))


def write_gen_report_curves(directory , dna , loss, perplexity, shape):
	# write our loss to csv file
	write_loss(directory, loss)
	write_dna(directory, dna)
	write_perplexity(directory,perplexity)
	write_shape(directory, shape)
	# calculate curve of best fit
	csv_target = directory / 'loss.csv'
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
	write_auc(directory, area_under_curve)

	x_new = np.linspace(x[0] , x[-1] , x[-1])
	y_new = f(x_new)

	# get name
	pltname = get_name_from_dir_path(directory)

	# plot the datapoints and the curve of best fit on top of it
	plt.plot(x,y,'b.')
	plt.plot(x_new,y_new,'m-',linewidth=3)
	filename = directory / pltname
	plt.savefig(str(filename))
	plt.clf()


# WARNING, this makes this program windows dependent
def get_name_from_dir_path(directory):
	strs = str(directory).split('\\')
	name = strs[-2] + '_' + strs[-1]
	return name
