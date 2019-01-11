from core import Parametric_tSNE
from pathlib import Path
from Genetics import Genetics
import pandas as pd
from tools import write_csv



test_data = "RBMTrainingDataset/2018_data.csv"
test_data_path = Path.cwd() / 'RBMTrainingDataset' / '2018_data.csv'
train_data_path = Path.cwd() / 'RBMTrainingDataset' / 'training_set.csv'
test_data = pd.read_csv(str(test_data_path) , sep=',' , header=None)
training_data = pd.read_csv(str(train_data_path) , sep=',' , header=None)
training_data = training_data.values
input_dims = test_data.shape[1]
test_data = test_data.values
output_dims = 2
save_path = Path.cwd() / 'model_load_test'


ptsne = Parametric_tSNE(input_dims, output_dims, 30)
ptsne.fit(training_data)
tform = ptsne.transform(test_data)
write_csv(tform , str(Path.cwd() / 'initial_tform.csv'))
ptsne.save_model(str(save_path))
ptsne.clear_session()




ptsne = Parametric_tSNE(input_dims , output_dims, 30)
ptsne.restore_model(str(save_path) , num_perplexities=30)

target_test_file = Path.cwd() / 'loaded_tform.csv'

predic = ptsne.transform(test_data)

write_csv(predic, str(target_test_file))
