# functions for evaluating generations of trained neural networks
import pandas as pd
import matplotlib.pyplot as plt
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
        # do i need to clear plot?
