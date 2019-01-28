import model_evaluation
from pathlib import Path
from tools import read_dna
from Genetics import Genetics

path_to_model_dir = Path.cwd() / "TestData" / "LongShallowGenTestCurve" / "generation_40" / "child_2"
path_to_data_file = Path.cwd() / "RBMTrainingDataset" / "2018_data.csv"
dna = read_dna(path_to_model_dir)
gh = Genetics()
perplexity , _ = gh.decode_dna(dna)

save_path = Path.cwd()
save_name = '40test.csv'

model_evaluation.model_evaluation(path_to_model_dir, path_to_data_file, save_path, save_name, output_dims=2)
