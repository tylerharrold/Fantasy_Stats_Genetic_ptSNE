from core import Parametric_tSNE
from pathlib import Path
import pandas as pd

datapath = Path.cwd() / 'RBMTrainingDataset' / 'training_set.csv'

data = pd.read_csv(str(datapath) , sep=',' , header=None)
high_dims = data.shape[1]
num_outputs = 2
perplexity = 30

target = str(Path.cwd() / 'Models' / 'testmodel')

ptsne = Parametric_tSNE(high_dims, num_outputs, perplexity)
ptsne.restore_model(target, num_perplexities=perplexity)

test_data = pd.read_csv(str(Path.cwd() / 'RBMTrainingDataset' / '2018_data.csv') , sep=',' , header=None)
test_data = test_data.values

x = ptsne.transform(test_data)

print(x)

print('fin')
