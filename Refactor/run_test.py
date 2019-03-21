# file containing master function that accepts areguments to runa multi
# generational ptsne training
import io_tools as io
import reporting
from pathlib import Path
from core import Parametric_tSNE
from Genetics import Genetics
import statistical_tools as stats
import evaluation as eval
'''
    inputs: testname                : name for the individual test
            num_gen                 : number of generations to run
            gen_size                : size of each individual generation
            train_data              : ndarray of data to train neural networks with
            train_data_name         : the name of the training data file
            test_data               : ndarray of data to test model with
            test_data_name          : the name of the test data file
            output_dim              : desired output dimensionality
            eval_type             : method with which to judge 'fitness' of models (SEE: evaluation.py)
            write_directory         : pathlib path to directory where all information will be stored for the test
            g_layers                : limit on number of layers a DNA string will contain
            g_layersize             : limit on size of an individual layer
            g_mutation_rate         : the rate of mutation that will occur in the DNA
            breed_method            : the way in which DNA will be bred together (SEE: Genetics)
            save_model              : whether or not the process will store trained models (Note: this consumes quite a bit of disk space depending on gensize and gennum)
            variable_mutation_rate  : whether the program will change mutation rate from generation to generation (THIS FEATURE NOT CURRENTLY IMPLEMENTED)

'''
def train(test_name , num_gen, gen_size, train_data , train_data_name , test_data , test_data_name , labels_data , labels_data_name , output_dim, eval_type, write_directory, g_layers=8, g_layersize=12 , g_mutation_rate=0.1,  breed_method="layerwise" , save_model=False , variable_mutation_rate=False):
    # setup directory in write_directory with the name of the test
    if not io.b_directory_exists(write_directory , test_name):
        test_dir = io.create_subfolder(write_directory , test_name)
    else:
        print("directory already exists with that name, quitting to avoid overwriting data")
        quit()

    # glean the input dimensionality from the training data
    input_dim = len(train_data[0])

    # within this directory, record the basic specs
    record_test_specs(test_dir , test_name , num_gen, gen_size , train_data_name , test_data_name , labels_data_name , eval_type , variable_mutation_rate , g_layers, g_layersize, breed_method, input_dim, output_dim)

    '''
    for generation in num_gen:
        setup generation subdir
        for child in generation:
            setup child folder
            train the network
            do analysis
            write reports
        evaluate best performers
        write generation analysis / reports (including best performers)
        breed new generation, change mutation rate if necessary
        fin
    '''

    # breed initial generation
    g = Genetics(maximum_possible_layers=g_layers , bits_per_layer=g_layersize)
    generation = g.breed_generation(gen_size)

    for i in range(num_gen):
        generation_name = "generation_" + str(i)
        first, second = train_generation(test_dir , generation_name , generation , input_dim , output_dim , train_data , test_data , labels_data , eval_type , verbose=False)
        generation = g.breed_generation(gen_size , [first,second])

    print("finished")

# records the test specs in the top test directory
def record_test_specs(test_dir , test_name , num_gen , gen_size, train_data_name , test_data_name , labels_data_name , eval_type , variable_mutation_rate , g_layers , g_layersize , breed_method, input_dim , output_dim):
    filename = test_name + "_report.json"
    reporting.write_json(test_dir , filename , test_name=test_name , num_gen=num_gen , gen_size=gen_size , train_data_name=train_data_name , test_data_name=test_data_name ,
        eval_type=eval_type , variable_mutation_rate=variable_mutation_rate , g_layers=g_layers , g_layersize=g_layersize , breed_method=breed_method, input_dim=input_dim , output_dim=output_dim , labels_data_name=labels_data_name)

# sets up the subdirectory for the training generation
# ~~~~~~~~~~~~~~~~~~~ TODO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def setup_generation_subdir():
    pass

# function in control of training a generation
def train_generation(test_dir , generation_name , generation, input_dim , output_dim , training_data , test_data , labels_data , eval_type , verbose=False):
    # setup the generation folder
    gen_dir = io.create_subfolder(test_dir , generation_name)

    # list of evaluations
    children_json = []

    # for each child in generation, train and get the evaluation for that individual, store these in a list
    number = 1
    for dna in generation:
        name = generation_name + "_child_" + str(number)
        train_child(gen_dir , name , input_dim , output_dim , dna , training_data , test_data , labels_data , eval_type , verbose=False)
        number = number + 1

    # write a generation report and save it in the generation folder
    #~~~~~~~~~~~~~~~~ TODO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # evaluate the generation and choose the best two
    first, second = eval.evaluate_generation(gen_dir , eval_type)
    return first , second

# train an individual child of a generation, returns json report on child
def train_child(gen_folder, child_name , input_dim , output_dim , dna , training_data , test_data , labels_data, eval_type , verbose=False):
    # setup folder
    child_folder = io.create_subfolder(gen_folder , child_name)
    # train ptsne
    perplexity , layers = Genetics.decode_dna(dna)
    print("#################### Training child of shape:" , str(layers) , "#########################################")
    ptsne = Parametric_tSNE(input_dim , output_dim , perplexity , all_layers=layers)
    losses = ptsne.fit(training_data , verbose=verbose)

    # tform test data
    tform = ptsne.transform(test_data)

    # TODO ------ save if necessary the model ------------

    # free memory
    ptsne.clear_session()

    # save data
    knn_error = stats.get_knn_error(tform , labels_data)
    if eval_type is "knn_error":
        eval_value = knn_error
    else:
        eval_value = eval.evaluate(eval_type , losses)
    report_name = "report.json"
    io.write_csv(child_folder , tform , "tform.csv")
    io.write_csv(child_folder , losses , "loss.csv")
    reporting.write_json(child_folder , report_name , child_name=child_name , input_dim=input_dim , output_dim=output_dim , perplexity=perplexity , layers=layers , knn_error=knn_error, DNA=dna , eval_value=eval_value , eval_type=eval_type)


if __name__ == "__main__":
    #record_test_specs(Path.cwd() , 'test1' , 10 , 20 , 'training_set.csv' , '2018-eos.csv' , 'half_auc' , False , 8 , 12 , 'layerwise')
    pass
