# Overall driver for rounds of genetic experimentation on ptsne network
# imports
import tools
from pathlib import Path
import os

from core import Parametric_tSNE
from report_writing import log_basic_test_params
import pandas as pd
import training_evaluation as eval
import Genetics


#TFORM_DATA = pd.read_csv(str(Path.cwd() / "RBMTrainingDataset" / "2018_data_eos.csv") , sep=',' , header=None).values
#TFORM_DATA = pd.read_csv(str(Path.cwd() / "Formatted_MNIST_Data" / "formatted_mnist_test.csv") , sep=',' , header=None).values
TFORM_DATA = pd.read_csv(str(Path.cwd() / "Normalized_Fantasy_Data" / "normalized_test_set.csv") , sep=',' , header=None).values

def train(num_generations, size_generation, base_directory, test_name,  data_path, output_dims=3, max_layers=8 , bits_per_layer=12, log=False, save_model=True, evaluation_type="curve" , seed=None):
    # instance genetic helper
    genetic_helper = Genetics.Genetics(max_layers , bits_per_layer, layer_crossbreed=True)
    # load dataset as ndarray
    test_data = tools.get_ndarray(data_path)
    # get dimensionality of dataset
    input_dims = len(test_data[0])
    # get initial gene pool
    if seed is None:
        gene_pool = genetic_helper.breed_generation(size_generation)
    else:
        gene_pool = genetic_helper.breed_generation(size_generation , seed)

    # setup test directory
    base_directory = tools.setup_file_structure(base_directory , test_name)

    # log the parameters of our test
    log_basic_test_params(base_directory , test_name , num_generations, size_generation, input_dims, output_dims, max_layers, bits_per_layer, evaluation_type)


    for generation in [i+1 for i in range(num_generations)]:
        generation_name = "generation_" + str(generation)
        resident_directory = base_directory / generation_name
        os.mkdir(str(resident_directory))
        run_generation(test_data, gene_pool, resident_directory, genetic_helper, input_dims, output_dims, generation_name, log, save_model)
        one_best, two_best = eval.evaluate(evaluation_type , resident_directory , log)
        gene_pool = genetic_helper.breed_generation(size_generation , [one_best , two_best])
        if log:
            print("Completed training of generation: " , generation_name)


def run_generation(test_data, gene_pool, resident_directory, genetic_helper, input_dims, output_dims, generation_name , log=False, save_model=True):
    for child_num, dna in [(i+1,j) for (i,j) in enumerate(gene_pool)]:
        child_name = "child_" + str(child_num)
        # make a folder for the child
        child_dir = resident_directory / child_name
        os.mkdir(str(child_dir))
        loss, model, tform = train_child(dna , genetic_helper, test_data, input_dims, output_dims, log)
        tools.write_loss(child_dir , loss)
        tools.write_dna(child_dir, dna)
        tools.write_csv(tform , (child_dir / "tform.csv"))
        if save_model:
            model.save_model(str(child_dir / "model"))
        if log:
            print(generation_name , " " , child_name , " trained")
        model.clear_session()

def train_child(dna , genetic_helper , test_data, input_dims, output_dims, log=False):
    perplexity, layers = genetic_helper.decode_dna(dna)
    if log:
        print("Training child with dim: " , str(layers))
    ptsne = Parametric_tSNE(input_dims, output_dims, perplexity, all_layers=layers)
    # train it on test_data
    loss = ptsne.fit(test_data, verbose=False)

    tform = ptsne.transform(TFORM_DATA)

    return loss, ptsne , tform

if __name__ == '__main__':
    #continue_dir = Path.cwd() / "TestData" / "normalized_fantasy_30_40_half_auc" / "generation_18"
    #best = eval._eval_half_curve(continue_dir)
    #seed = [best[0] , best[1]]
    #run_test(40,5,'LongShallowGenTestCurve','TestData' , "RBMTrainingDataset/training_set.csv" , 2)
    train(30, 40 , 'TestData' , 'normalized_fantasy_3D_30_40_half_auc' , 'Normalized_Fantasy_Data/normalized_training_set.csv' , log=True , save_model=False , evaluation_type="half_curve")
