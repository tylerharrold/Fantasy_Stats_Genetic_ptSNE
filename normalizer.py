import pandas as pd
from pathlib import Path
from tools import write_csv

training_dataset_path = Path.cwd() / 'RBMTrainingDataset' / 'training_set.csv'

normalized_path = Path.cwd() / 'Normalized_Training_Data' / 'training_set_normalized.csv'

# import un-normalized training data
df = pd.read_csv(str(training_dataset_path) , sep=',' , header=None)

df_norm = ((df - df.min()) / (df.max() - df.min()))

df_norm.to_csv(path_or_buf=str(normalized_path) , sep=',' , index=False, header=None)
