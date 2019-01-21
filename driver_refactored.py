# Overall driver for rounds of genetic experimentation on ptsne network
# imports
import tools
from pathlib import Path
import os

from core import Parametric_tSNE
import pandas as pd
import training_evaluation as eval
import Genetics

def train(num_generations, size_generation, base_directory, data_path, output_dims=2, max_layers=8 , bits_per_layer=12, log=False, save_model=True, evaluation_type="curve"):
    # instance genetic helper
    genetic_helper = Genetics(max_layers , bits_per_layer)
    # load dataset as ndarray
    data = tools.get_ndarray(data_path)
    # get dimensionality of dataset
    input_dims = len(data[0])
    # get initial gene pool
    gene_pool = genetic_helper.breed_generation(size_generation)

    for generation in [i+1 for i in range(num_generations)]:
        generation_name = "generation_" + str(generation)
        resident_directory = base_directory / generation_name
        os.mkdir(str(resident_directory))
        run_generation(gene_pool, resident_directory, genetic_helper, input_dims, output_dims, log, save_model)
        one_best, two_best = eval.evaluate(evaluation_type , resident_directory)
        gene_pool = genetic_helper.breed_generation(size_generation , [one_best , two_best])
        if log:
            print("Completed training of generation: " , generation_name)


def run_generation(gene_pool, resident_directory, genetic_helper, input_dims, output_dims, log=False, save_model=True):
    for child_num, dna in [(i+1,j) for (i,j) in enumerate(gene_pool)]:
        child_name = "child_" + str(child_num)
        # make a folder for the child
        child_dir = resident_directory / child_name
        os.mkdir(str(child_dir))
        loss, model = train_child(dna , genetic_helper, data, input_dims, output_dims, log)
        tools.write_loss(child_dir , loss)
        if save_model:
            model.save_model(str(child_dir / "model"))
        if log:
            print(generation_name , " " , child_name , " trained")
        model.clear_session()

def train_child(dna , genetic_helper , data, input_dims, output_dims, log=False):
    perplexity, layers = genetic_helper.decode_dna(dna)
    if log:
        print("Training child with dim: " , str(layers))
    ptsne = Parametric_tSNE(input_dims, output_dims, perplexity, all_layers=layers)
    # train it on test_data
    loss = ptsne.fit(test_data, verbose=False)

    return loss, ptsne

if __name__ == '__main__':
    run_test(40,5,'LongShallowGenTestCurve','TestData' , "RBMTrainingDataset/training_set.csv" , 2)
