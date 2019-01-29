import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from tools import read_dna
import pandas as pd
from Genetics import Genetics
from core import Parametric_tSNE

def load_train_model_from_dna(model_save_name, output_dims=2):
    current_dir = Path.cwd()
    dna_file = filedialog.askopenfilename(initialdir = str(current_dir) , title="Select DNA file")
    save_folder = filedialog.askdirectory(initialdir = str(current_dir) , title="Select folder to save model")

    data_file = Path.cwd() / "RBMTrainingDataset" / "training_set.csv"

    test_data = pd.read_csv(str(data_file) , sep=',' , header=None).values
    input_dims = len(test_data[0])

    dna = Path(str(dna_file)).read_text()

    genetic_helper = Genetics()
    perplexity, layers = genetic_helper.decode_dna(dna)

    save = Path(save_folder)
    save_path = save / model_save_name

    ptsne = Parametric_tSNE(input_dims, output_dims, perplexity, all_layers=layers)
    loss = ptsne.fit(test_data, verbose=False)
    ptsne.save_model(str(save_path))



if __name__ == "__main__":
    load_train_model_from_dna("long_half_curve_gen_40_child_1.model")
