# file with functions used to evaluate 'fitness' of trained models with regards
# to other trained models in a given generation
import numpy as np
import json

# controller function that returns the appropriate result given the specified eval_type
def evaluate(eval_type , losses):
    if eval_type is "linear":
        return get_linear_evaluation(losses)
    elif eval_type is "auc":
        return get_area_under_curve(losses)
    elif eval_type is "half_auc":
        return get_area_under_half_curve(losses)
    else:
        print("error in evaluation type selection, returning dummy value")
        return -1


# method used to evaluate linear performance of loss
def get_linear_evaluation(losses):
    return -1 # dummy value for now

# method used to evaluate area under curve performance of loss
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

# method used to evaluate area under last half of the cureve of loss
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

# method that looks at a list of child evaluations and returns the best two
def evaluate_generation(resident_directory , evaluation_type):
    if evaluation_type is "curve":
        return _eval_curve(resident_directory)
    elif evaluation_type is "half_auc":
        return _eval_half_curve(resident_directory)
    elif evaluation_type is "linear":
        return _eval_linear(resident_directory)
    elif evaluation_type is "knn_error":
        return _eval_knn(resident_directory)
    else:
        print("critical error, evaluation type not correctly specified")

# evaluates the children of a generation by their recorded losses
# calculates the area under the curve fitted to those losses and returns the
# lowest two
def _eval_curve(resident_directory):
    # iterate through the subfolders (child folders) in resident_directory
    areas = []
    for dir in [x for x in resident_directory.iterdir() if x.is_dir()]:
        with open(str(dir / "report.json")) as json_file:
            data = json.load(json_file)
        areas.append((data["eval_value"] , data['DNA']))
    areas.sort(key=lambda x: x[0])
    return areas[0][1] , areas[1][1]

# evaluates the children of a generation by their recorded losses
# calculates the area under half of the curve fitted to those losses and returns the
# lowest two
def _eval_half_curve(resident_directory):
    # iterate through the subfolders (child folders) in resident_directory
    areas = []
    for dir in [x for x in resident_directory.iterdir() if x.is_dir()]:
        with open(str(dir / "report.json")) as json_file:
            data = json.load(json_file)
        areas.append((data["eval_value"] , data['DNA']))
    areas.sort(key=lambda x: x[0])
    return areas[0][1] , areas[1][1]

def _eval_variance(resident_directory):
    pass

def _eval_area_variance_vector(resident_directory):
    pass

def _eval_linear(resident_directory):
    pass

def _eval_knn(resident_directory):
    # iterate through the subfolders (child folders) in resident_directory
    areas = []
    for dir in [x for x in resident_directory.iterdir() if x.is_dir()]:
        with open(str(dir / "report.json")) as json_file:
            data = json.load(json_file)
        areas.append((data["knn_error"] , data['DNA']))
    areas.sort(key=lambda x: x[0])
    return areas[0][1] , areas[1][1]
