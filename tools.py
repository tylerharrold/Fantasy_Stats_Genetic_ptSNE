import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import os
# need a function to write out the transformed data to a csv
# NOTE this function should be altered to write datafile into a specific directory
def write_csv(input_data, specified_filename):

	# turn input_data into a pandas dataframe
	df = pd.DataFrame(input_data)

	# write it out
	df.to_csv(path_or_buf=str(specified_filename) , sep=',' , index=False, header=None)

# given a path to a csv file, returns ndarray of data
def get_ndarray(csv_path):
	data = pd.read_csv(str(csv_path) , sep=',' , header=None)
	return data.values

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

# reads dna as string from directory
def read_dna(directory):
	path = directory / 'dna.dna'
	return path.read_text()

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
	csv = pd.read_csv(str(path) , sep=',' , header=None)
	return csv.values[0]

def write_perplexity(directory, perplexity):
	path = directory / 'perplexity.txt'
	path.write_text(str(perplexity))

def write_shape(directory, shape):
	path = directory / 'shape.txt'
	path.write_text(str(shape))

# function that, given a list of losses, fits a curve to the losses and returns
# the integral of the function of that curve
# params: losses -- a 1d array of loss values
def get_area_under_curve(losses):
	points = [(x,y) for x,y in enumerate(losses)]
	x = [x for x,y in points]
	y = [y for x,y in points]

	z = np.polyfit(x, y, 2)
	f = np.poly1d(z)
	f_prime = np.polyint(f)
	# we are always integrating from x[-1], the max x coordinate, to 0, so we only are concerned about the max value for def integral
	area_under_curve = f_prime(x[-1])
	return area_under_curve

# function that, given a list of losses, fits a curve to the losses and returns
# the integral of the function of that curve over the second half of curve
# in essence returning the area under the loss curve for the latter stages of the
# model training
# params: losses -- a 1d array of loss values
def get_area_under_half_curve(losses):
	points = [(x,y) for x,y in enumerate(losses)]
	x = [x for x,y in points]
	y = [y for x,y in points]

	num_points = len(x)

	z = np.polyfit(x, y, 2)
	f = np.poly1d(z)
	f_prime = np.polyint(f)
	# we are always integrating from x[-1], the max x coordinate, to 0, so we only are concerned about the max value for def integral
	area_under_curve = f_prime(x[-1]) - f_prime(x[num_points//2])
	return area_under_curve


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

def setup_file_structure(base_dir_name , test_name):
	active_dir = Path.cwd()
	base_dir = active_dir / base_dir_name
	if base_dir not in [x for x in active_dir.iterdir() if x.is_dir()]:
		os.mkdir(str(base_dir_name))
	test_dir = base_dir / test_name
	if test_dir in [x for x in base_dir.iterdir() if x.is_dir()]:
		print("ERROR: directory already exists with desired test name....quitting...")
		quit()
	else:
		os.mkdir(str(base_dir / test_name))
	test_dir = base_dir / test_name
	return test_dir
