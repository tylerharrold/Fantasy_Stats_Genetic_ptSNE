from core import Parametric_tSNE
from pathlib import Path
from Genetics import Genetics
import pandas as pd
from tools import write_csv



test_data = "RBMTrainingDataset/2018_data.csv"
test_data_path = Path.cwd() / 'RBMTrainingDataset' / '2018_data.csv'
data = pd.read_csv(str(test_data_path) , sep=',' , header=None)
input_dims = data.shape[1]
print(input_dims)
data = data.values
print(data.shape)
output_dims = 2

load_target = Path.cwd() / 'TestData' / 'Area_Eval_Test' / 'generation_1' / 'child_1'

dna_path = load_target / 'dna.dna'

dna = dna_path.read_text()

g = Genetics(8 , 12)
perplexity , layers = g.decode_dna(dna)

model_path = load_target / 'model'

ptsne = Parametric_tSNE(input_dims , output_dims, perplexity)
ptsne.restore_model(str(model_path) , num_perplexities=perplexity)

target_test_file = Path.cwd() / 'test_predic.csv'

predic = ptsne.transform(data)

write_csv(predic, str(target_test_file))
