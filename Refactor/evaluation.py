# file with functions used to evaluate 'fitness' of trained models with regards
# to other trained models in a given generation
import numpy as np

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
