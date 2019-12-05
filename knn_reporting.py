from pathlib import Path
import pandas as pd
import numpy as np
import json
from tools import get_ndarray

'''
Tools for evaluating the performance of a parametric t-SNE network based on the single k-nearest neighbor for each
reduced point compared to the actual known value of a transformed point

e.g. a point is classified as 'correctly' mapped if it's nearest neighbor is of the same label type as it, and
	'incorrect' if it is paired most closely with something of a different type

'''


# calculate euclidian distances between two points in d-dimensional space
# NOTE - points must be passed in as a list or tuple of values e.g. [x,y,z] or (x,y,z)
def _get_euclidian_dist(point_1 , point_2 , data_dim):
	distance = 0
	for x in range(data_dim):
		distance += np.square(point_1[x] - point_2[x])
	return np.sqrt(distance)

# given a tform and labels (as values), perform a knn analysis
def avg_knn_error(tform , labels , labels_identifying_col):

	assert len(tform) == len(labels)
	# get the dimensions of tform
	data_dim = len(tform[0])

	# table of distances between each point and every other point in tform
	# a value of NONE will be inserted into the table when a point is compared
	# with itself
	dist_matrix = []
	for i in range(len(tform)):
		row = []
		for j in range(len(tform)):
			if i == j:
				row.append(None)
			else:
				row.append(_get_euclidian_dist(tform[i] , tform[j] , data_dim))
		dist_matrix.append(row)

	accuracy_matrix = []
	for row in range(len(dist_matrix)):
		lowest_index = -1
		for column in range(len(dist_matrix)):
			if dist_matrix[row][column] is not None: #i.e. it is not itself
				dist = dist_matrix[row][column]
				if lowest_index < 0:
					lowest_index = column
				else:
					if dist < dist_matrix[row][lowest_index]:
						lowest_index = column

		pred_v_true = []
		pred_v_true.append(labels[lowest_index][labels_identifying_col])
		pred_v_true.append(labels[row][labels_identifying_col])
		accuracy_matrix.append(pred_v_true)

	errors = 0

	for i in accuracy_matrix:
		print(i[0] , ' ' , i[1])
		if i[0] is not i[1]:
			errors = errors + 1

	n = len(accuracy_matrix)

	error_pctg = errors / n
	return error_pctg

# for a generation, write a json report of errors
def create_gen_knn_error_json(root_folder , labels_file , labels_identifying_col , title):
	data = {}
	generational_error = 0
	num_children = 0
	for child in [x for x in root_folder.iterdir() if x.is_dir()]:
		num_children += 1
		name = child.name
		tform = pd.read_csv(str(child / "tform.csv") , sep=',' , header=None).values
		labels = pd.read_csv(str(labels_file) , sep=',' , header=None).values
		knn_error = avg_knn_error(tform , labels , labels_identifying_col)
		data[name] = {'knn_error':knn_error}
		generational_error += knn_error
	data['avg_knn_error'] = generational_error / num_children

	with open(str(root_folder / ('knn_eval_' + title + '.json')) , 'w') as outfile:
		json.dump(data, outfile)

def create_test_knn_error_reports(root_test_folder , labels_file , labels_identifying_col , title):
	for generation in [x for x in root_test_folder.iterdir() if x.is_dir()]:
		create_gen_knn_error_json(generation , labels_file , labels_identifying_col , title)


if __name__ == "__main__":
	#knn reports for normalized combine 3d trained
	#				normalized combine 3d flat
	#				normalized combine 2d trained
	#				normalized comgine 2d flat
	#				normalized fantasy 2d flat
	#				normalized fantasy 2d trained
	'''
	combine_labels_file = Path.cwd() / "NFL_Combine_Data" / "2019Both.csv"
	combine_labels_identifying_col = 1
	fantasy_labels_file = Path.cwd() / "RBMTrainingDataset" / "2018_labels_eos.csv"
	fantasy_labels_identifying_col = 1
	norm_com_3d_trained  = Path.cwd() / "TestData" / "normalized_combine_3D_30_40_half_auc"
	norm_com_3d_flat  = Path.cwd() / "TestData" / "normalized_combine_3D_flat_40"
	norm_com_2d_trained  = Path.cwd() / "TestData" / "normalized_combine_30_40_half_auc"
	norm_com_2d_flat = Path.cwd() / "TestData" / "normalized_combine_flat_40_half_auc"
	norm_fant_2d_flat = Path.cwd() / "TestData" / "normalized_fantasy_flat_40_half_auc"
	norm_fant_2d_trained = Path.cwd() / "TestData" / "normalized_fantasy_30_40_CONTINUED_half_auc"

	test_list = [
		(norm_com_3d_trained , combine_labels_file , combine_labels_identifying_col) ,
		(norm_com_3d_flat , combine_labels_file , combine_labels_identifying_col) ,
		(norm_com_2d_trained , combine_labels_file , combine_labels_identifying_col) ,
		(norm_com_2d_flat , combine_labels_file , combine_labels_identifying_col)
		#(norm_fant_2d_flat , fantasy_labels_file , fantasy_labels_identifying_col) ,
		#(norm_fant_2d_trained , fantasy_labels_file , fantasy_labels_identifying_col)
	]
	for sublist in test_list:
		create_test_knn_error_reports(sublist[0] , sublist[1] , sublist[2] , 'positional')
	'''
	# for flat 40 3d fantasy
	create_test_knn_error_reports((Path.cwd() / "TestData" / "normalized_fantasy_3D_flat_40_half_auc") , (Path.cwd() / "RBMTrainingDataset" / "2018_labels_eos.csv"),1 , "positional")
	# for 30-40 3d fantasy
	create_test_knn_error_reports((Path.cwd() / "TestData" / "normalized_fantasy_3D_30_40_half_auc") , (Path.cwd() / "RBMTrainingDataset" / "2018_labels_eos.csv"),1 , "positional")
