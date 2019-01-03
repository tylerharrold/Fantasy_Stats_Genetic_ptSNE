import pandas as pd
from pathlib import Path
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

# write loss data in specified directory in csv
def write_loss(directory, loss):
	path = directory / 'loss.csv'
	path.write_text(str(loss).strip('[]'))

# reads loss from folder path and returns list
# Note, needs fixing
def read_loss(directory):
	path = directory / 'loss.csv'
	return list(path.read_text())
