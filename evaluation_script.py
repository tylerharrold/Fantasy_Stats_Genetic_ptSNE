# A general purpose script for evaluating and graphing the overall performance
# and testing results for various models
from pathlib import Path


# Parameters

NUM_MODELS = 9
GENERATION_DIR = Path.cwd() / "TestData" / "half_curve_layer_swap_flat_40" / "generation_1"
SAVE_DIR = Path.cwd() / "Analysis" / "HCLSFlat40"

# Get a Generation Report

# Get full json of Generation Report and Randomly select 9 of the models

# For each of the 9 models, graph their loss performance with evaluation curve overlaid  and save these named appropriately

# for each of the 9 models, using DNA, retrain using training dataset, get a transform of test data, then create a plotly for that transform, save this
