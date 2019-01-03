from core import Parametric_tSNE
import pandas as pd
from pathlib import Path
import tools
import genetic_helpers as gh

datapath = Path.cwd() / 'RBMTrainingDataset' / 'training_set.csv'
small_dataset = Path.cwd() / 'RBMTrainingDataset' / '2017_data.csv'

data = pd.read_csv(str(small_dataset) , sep=',' , header=None)
high_dims = data.shape[1]
num_outputs = 2
perplexity = 30

train_data = data.values

#test_data = pd.read_csv(str(Path.cwd() / 'RBMTrainingDataset' / '2018_data.csv') , sep=',' , header=None)
#test_data = test_data.values

dna = gh.generate_blueprint()
perplexity, layers = gh.decode_blueprint(dna)
print(perplexity)
print(layers)

ptSNE = Parametric_tSNE(high_dims, num_outputs, perplexity, all_layers=None)
ptSNE.fit(train_data, verbose=1)

ptSNE.clear_session()
#x = ptSNE.transform(test_data)
#tools.write_csv(x , 'transformed_data.csv')

#ptSNE.save_model(str(Path.cwd() / 'Models' / 'testmodel'))

print('done')
