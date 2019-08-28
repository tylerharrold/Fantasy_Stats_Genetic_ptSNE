import tools
from pathlib import Path
import os

from core import Parametric_tSNE
from report_writing import log_basic_test_params
import pandas as pd
import training_evaluation as eval
import Genetics

# import mnist data and ensure its in a workable format (i think i already did this legwok)
train_data = pd.read_csv(str(Path.cwd() / 'Formatted_MNIST_Data' / 'formatted_mnist_train.csv') , sep=',' , header=None).values
test_data = pd.read_csv(str(Path.cwd() / 'Formatted_MNIST_Data' / 'formatted_mnist_test.csv') , sep=',' , header=None).values

# instance a ptsne network and train the dataset using training data
ptsne = Parametric_tSNE(784 , 2 , 30)
print("starting to train...")
loss = ptsne.fit(train_data , verbose=True)
print('done training....')
tform = ptsne.transform(test_data)

save_path = Path.cwd() / 'MNIST_testing'

tools.write_loss(save_path , loss)
tools.write_csv(tform , (save_path / "tform.csv"))



# graph and save
