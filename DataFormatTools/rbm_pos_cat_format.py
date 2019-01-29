# script that formats our raw fantasy football data into a format for categorization by our RBM
# this data will split the headers from the raw numbers, and also remove the data
# that lists fantasy output (seeing as we want our analysis to be potentially fantasy
# relevant, it seems inappropriate to include overall fantasy ranking in the dataset)

# necessary imports
import pandas as pd 
import os
from pathlib import Path

# ability to iterate through every file that begins with a yearin the Raw_Fantasy_Data 
#	folder
dir_path = os.path.dirname(os.path.realpath(__file__))
DATA_DIR_NAME = 'RawFantasyData'

# get the parent of the current working directory
if dir_path[-1] is not '/' : dir_path = dir_path + '/'
parent_dir = str(Path(dir_path).parent)

# get a handle for the data directory we want to access
if parent_dir[-1] is not '/' : parent_dir = parent_dir + '/'
data_dir = parent_dir + DATA_DIR_NAME 

# get all the files in our RawFantasyData folder (in python list)
data_filenames = os.listdir(path=data_dir) 

# for each file, split the header away and save to our chosen directoyr, remove the fantasy
# ----

# pull in raw data as pandas DF, but I need to add the labels to it (stored in labels_for_raw.csv)
HEADER_FILE = 'header_for_raw.csv'


# pull our header data
if data_dir[-1] is not '/' : data_dir = data_dir + '/'
header_path = data_dir + HEADER_FILE
headers = pd.read_csv(header_path , sep=',' , header=None)
header_values = headers.values[0]

# Directory for formatted data
FORMATTED_DATA_DIR = 'FormattedFantasyData/'
FORMATTED_DATA_PATH = parent_dir + FORMATTED_DATA_DIR

# we no longer want 'header_for_raw.csv' in our list of files
data_filenames.remove('header_for_raw.csv')

#iterate through each raw data file, pull out labels and save them, pull out fant data and save nums
for filename in data_filenames:
	# grab year prefix for naming files
	prefix = filename[:5] # this will end with _
	print(prefix)

	full_filepath = data_dir + filename 
	df = pd.read_csv(full_filepath , sep=',' , header=None)
	# assign our headers to the dataframe
	df.columns = header_values 

	# a list of column names pertaining to labels
	label_columns = ['name','team','position'] # this list gives us the label dataframe to produce
	# a list of fantasy stats to exluce
	fantasy_columns = ['standard_pts','ppr_points','draft_king_points','fan_duel_points','vbd','position_rank','overall_rank']
	
	# get our labels only dataframe and save it
	labels_df = df[label_columns]
	fullname = FORMATTED_DATA_PATH + prefix + 'labels.csv'
	labels_df.to_csv(fullname , sep=',', index=False, header=None)

	# get a list of data we want that excludes both label columns and fantasy columns
	blacklist = label_columns + fantasy_columns
	whitelist = [item for item in header_values if item not in blacklist]
	formatted_data = df[whitelist]
	fullname = FORMATTED_DATA_PATH + prefix + 'data.csv'
	formatted_data.to_csv(fullname , sep=',', index=False, header=None)

print('data formatting complete')

	




# -----

# example of how this can be split in pandas


#	data and store the numbers in the same folder under a raw.csv file