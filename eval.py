# functions for evaluating generations of trained neural networks
import pandas as pd
import matplotlib.pyplot as plt
from tools import get_name_from_dir_path as get_name
# function that returns the bitstrings of the two best performing models
# this function looks at all models contained within generation generation_directory
# and returns the
def eval_using_last_loss(generation_directory):
    losses = []
    for dir in [x for x in generation_directory.iterdir() if x.is_dir()]:
        csv_file = dir / 'loss.csv'
        csv = pd.read_csv(str(csv_file) , sep=',' , header=None)
        last_loss = csv.values[0][-1]
        dna_file = dir / 'dna.dna'
        dna = dna_file.read_text()
        losses.append( (last_loss , dna) )
    losses.sort(key=lambda x: x[0])
    return losses[0][1] , losses[1][1]


def eval_using_area_under_curve(generation_directory):
    # get the name and the area under curve for each child in this directory
    areas = []
    for dir in [x for x in generation_directory.iterdir() if x.is_dir()]:
        area_file = dir / 'auc.txt'
        area_val = float(area_file.read_text())
        child_name = get_name(dir)
        dna_file = dir / 'dna.dna'
        dna = dna_file.read_text()
        areas.append( (area_val , dna , child_name))
    areas.sort(key=lambda x: x[0])
    generate_generation_report(generation_directory , areas)
    return areas[0][1] , areas[1][1]

def generate_generation_report(generation_directory , values):
    file = generation_directory / 'performance.txt'
    built_string = ''
    for v in values:
        built_string = built_string + str(v) + '\n'
    file.write_text(built_string)

# generates a report for the performance of the members of the generation
def generate_generation_perf_report(generation_directory):
    for dir in [x for x in generation_directory.iterdir() if x.is_dir()]:
        csv_file = dir / 'loss.csv'
        csv = pd.read_csv(str(csv_file) , sep=',' , header=None)
        vals = csv.values[0]
        plt.plot(vals , 'b.')
        plt.ylabel('loss')
        filename = dir / 'plot.png'
        plt.savefig(str(filename))
        plt.clf()
        # do i need to clear plot?
