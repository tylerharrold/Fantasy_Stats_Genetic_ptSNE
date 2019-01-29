import os
import pandas as pd 
from pathlib import Path


DATA_DIR = 'FormattedFantasyData/'
TARGET_DIR = 'RBMTrainingDataset/'

# from ../FormattedFantasyData, grab every [year]_data.csv file

# get our current directory
current_dir = os.path.dirname(os.path.realpath(__file__))
if current_dir[-1] is not '/' : current_dir = current_dir + '/'

# get a handle for the data directory we want to access
parent_dir = str(Path(current_dir).parent)
if parent_dir[-1] is not '/' : parent_dir = parent_dir + '/'
data_path = parent_dir + DATA_DIR

# get all the files in our RawFantasyData folder (in python list)
data_filenames = os.listdir(path=data_path) 
# we are not using 2018 data for training, so just remove it
data_filenames.remove('2018_data.csv')

# get string name for target file in target directory
target_filename = parent_dir + TARGET_DIR + 'training_set.csv'

# draw them all into dataframes and write to csv, appending as we go
counter = 0
for filename in data_filenames:
	if 'labels' not in filename:
		filepath = data_path + filename
		df = pd.read_csv(filepath , sep=',' , header=None)
		with open(target_filename , 'a') as f:
			df.to_csv(f , sep=',' , header=None , index=False)
		
