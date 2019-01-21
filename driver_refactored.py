# Overall driver for rounds of genetic experimentation on ptsne network
# imports
import tools
from pathlib import Path
import os

from core import Parametric_tSNE
import pandas as pd
import eval
import Genetics

def train():
    for gen in range(num_generations):
        run_generation()

def run_generation(genetics):
    pass


# run the breeding for GENERATIONS with GENSIZE with TESTNAME in DIRNAME
def run_test(num_generations , gensize , testname , target_dir_name, test_data, output_dims, max_layers=8 , bits_per_layer=12):

    gh = Genetics.Genetics(max_layers , bits_per_layer)

    # create the target directory if it doesn't exist
    current_dir = Path('.')
    target_dir = Path('.') / target_dir_name

    if target_dir not in [x for x in current_dir.iterdir() if x.is_dir()]:
        os.mkdir(str(target_dir))

    # create directory in target_dir named for this test, but quit if
    # this directory already exists as we don't want accidental overwrites

    #NOTE we don't care about overwrites now so this is commented out, uncomment when driver is finished
    test_dir = target_dir / testname
    if test_dir in [x for x in target_dir.iterdir() if x.is_dir()]:
        print("ERROR: a directory of this test name already exists, quitting to avoid potential overwrites...")
        quit()
    else:
        os.mkdir(str(test_dir))
    '''
    if test_dir not in [x for x in target_dir.iterdir() if x.is_dir()]:
        os.mkdir(str(test_dir)) # delete when the above lines are uncommented
    '''

    # load test data
    test_data_file = current_dir / test_data
    data = pd.read_csv(str(test_data_file) , sep=',' , header=None)
    input_dims = data.shape[1]
    data = data.values

    # create a file to sit in our test_dir that describes the sizes of the test,
    # for ease of future reading, this will be called 'test_specs'
    tools.write_test_specs(test_dir, num_generations, gensize)

    # get our first batch of dna
    child_dna = gh.breed_generation(gensize)

    # for reasons of directory nomenclacture, we use 1 as our base index
    for generation in [i+1 for i in range(num_generations)]:
        generation_name = 'generation_' + str(generation)
        # create a directory for this generation
        gen_dir = test_dir / generation_name
        os.mkdir(str(gen_dir))
        # same thing with children
        for child_num, dna in [(i+1,j) for (i,j) in enumerate(child_dna)]:
            child_name = "child_" + str(child_num)
            # make a folder for the child
            child_dir = gen_dir / child_name
            os.mkdir(str(child_dir))
            train_child(child_dir , dna , data, input_dims, output_dims, gh)
            print(generation_name , " " , child_name , " trained")

        # now that children are trained, get the best two
        one, two = eval.eval_using_area_under_curve(gen_dir)
        # generate graphs for our children
        #eval.generate_generation_perf_report(gen_dir)
        # use best two to breed
        child_dna = gh.breed_generation(gensize , [one,two])
        print(generation_name , ' Finished...beginning new generation')

# function that handles the training of a specific child and writes out its data
def train_child(child_dir_path , dna, test_data, input_dims, output_dims , gh):
    # translate our dna
    perplexity, layers = gh.decode_dna(dna)
    print("training child of dim: " , layers)
    # create a network of this name with our stats
    ptsne = Parametric_tSNE(input_dims, output_dims, perplexity, all_layers=layers)
    # train it on test_data
    loss = ptsne.fit(test_data, verbose=False)
    # save our model
    model_path = child_dir_path / 'model'
    ptsne.save_model(str(model_path))
    # write our loss, dna, and save a graph of performance
    tools.write_gen_report_curves(child_dir_path , dna , loss, perplexity, layers)
    ptsne.clear_session()

# given the name of a generation, analyze it
def analyze_generation():
    pass



if __name__ == '__main__':
    run_test(40,5,'LongShallowGenTestCurve','TestData' , "RBMTrainingDataset/training_set.csv" , 2)
