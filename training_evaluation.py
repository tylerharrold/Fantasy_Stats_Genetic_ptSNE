from tools import read_loss
from tools import read_dna
from tools import get_area_under_curve
from tools import get_area_under_half_curve

def evaluate(evaluation_type , resident_directory , log=False):
    if evaluation_type is "curve":
        if log : print("evaluating using area under curve")
        return _eval_curve(resident_directory)
    if evaluation_type is "half_curve":
        if log : print("evaluating using area under half curve")
        return _eval_half_curve(resident_directory)
    else:
        print("error, invalid evaluation type")

# evaluates the children of a generation by their recorded losses
# calculates the area under the curve fitted to those losses and returns the
# lowest two
def _eval_curve(resident_directory):
    # iterate through the subfolders (child folders) in resident_directory
    areas = []
    for dir in [x for x in resident_directory.iterdir() if x.is_dir()]:
        losses = read_loss(dir)
        dna = read_dna(dir)
        area_under_curve = get_area_under_curve(losses)
        areas.append((area_under_curve , dna))
    areas.sort(key=lambda x: x[0])
    return areas[0][1] , areas[1][1]

# evaluates the children of a generation by their recorded losses
# calculates the area under half of the curve fitted to those losses and returns the
# lowest two
def _eval_half_curve(resident_directory):
    # iterate through the subfolders (child folders) in resident_directory
    areas = []
    for dir in [x for x in resident_directory.iterdir() if x.is_dir()]:
        losses = read_loss(dir)
        dna = read_dna(dir)
        area_under_curve = get_area_under_half_curve(losses)
        areas.append((area_under_curve , dna))
    areas.sort(key=lambda x: x[0])
    return areas[0][1] , areas[1][1]

def _eval_variance(resident_directory):
    pass

def _eval_area_variance_vector(resident_directory):
    pass

def _eval_linear(resident_directory):
    pass
