from pathlib import Path
import Genetics_Refactored as G
import tools
from core import Parametric_tSNE

# go through our flat 40 data
# use the info we have to retrain a model of that shape and structure
# get a tranform and save it


TARGET_FOLDER = Path.cwd() / "TestData" / "half_curve_layer_swap_40" / "generation_30"
SAVE_FOLDER = Path.cwd() / "Bred40_Tforms"
TRAINING_DATA = Path.cwd() / "RBMTrainingDataset" / "training_set.csv"
TEST_DATA = Path.cwd() / "RBMTrainingDataset" / "2018_data_eos.csv"

test_data = tools.get_ndarray(TEST_DATA)
input_dims = len(test_data[0])

train_data = tools.get_ndarray(TRAINING_DATA)

output_dims = 2

gh = G.Genetics()

for child in [c for c in TARGET_FOLDER.iterdir() if c.is_dir()]:
    # get the perp and layer sturcure for this child
    dna_string = tools.read_dna(child)
    perp, layers = gh.decode_dna(dna_string , legacy_dna=True)
    # train this model
    ptsne = Parametric_tSNE(input_dims, output_dims, perp, all_layers=layers)
    _ = ptsne.fit(train_data, verbose=False)
    transform = ptsne.transform(test_data)
    save_path = SAVE_FOLDER / (child.name + "_tform.csv")
    tools.write_csv(transform , save_path)
    ptsne.clear_session()
