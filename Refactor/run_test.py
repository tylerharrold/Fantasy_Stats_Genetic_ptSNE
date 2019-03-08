# file containing master function that accepts areguments to runa multi
# generational ptsne training
import io_tools as io
import reporting
from pathlib import Path
from core import Parametric_tSNE
from Genetics import Genetics as G
import statistical_tools as stats
'''
    inputs: testname                : name for the individual test
            num_gen                 : number of generations to run
            gen_size                : size of each individual generation
            train_data              : ndarray of data to train neural networks with
            train_data_name         : the name of the training data file
            test_data               : ndarray of data to test model with
            test_data_name          : the name of the test data file
            output_dim              : desired output dimensionality
            eval_method             : method with which to judge 'fitness' of models (SEE: evaluation.py)
            write_directory         : pathlib path to directory where all information will be stored for the test
            g_layers                : limit on number of layers a DNA string will contain
            g_layersize             : limit on size of an individual layer
            g_mutation_rate         : the rate of mutation that will occur in the DNA
            breed_method            : the way in which DNA will be bred together (SEE: Genetics)
            save_model              : whether or not the process will store trained models (Note: this consumes quite a bit of disk space depending on gensize and gennum)
            variable_mutation_rate  : whether the program will change mutation rate from generation to generation (THIS FEATURE NOT CURRENTLY IMPLEMENTED)

'''
def train(test_name , num_gen, gen_size, train_data , train_data_name , test_data , test_data_name , labels_data , labels_data_name , output_dim, eval_method, write_directory, g_layers, g_layersize , g_mutation_rate,  breed_method="layerwise" , save_model=False , variable_mutation_rate=False):
    # setup directory in write_directory with the name of the test
    if not io.b_directory_exists(write_directory , test_name):
        test_dir = io.create_subfolder(write_directory , test_name)
    else:
        print("directory already exists with that name, quitting to avoid overwriting data")
        quit()

    # glean the input dimensionality from the training data
    input_dim = len(train_data[0])

    # within this directory, record the basic specs
    record_test_specs(test_dir , test_name , num_gen, gen_size , train_data_name , test_data_name , labels_data_name , eval_method , variable_mutation_rate , g_layers, g_layersize, breed_method, input_dim, output_dim)

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
    for generation in range(num_gen):
        setup_generation_subdir()
        for child in range(gen_size):
            train_child()
        evaluate_best_performers()
        write_generational_reports()
        breed_new_generation()

    pass

# records the test specs in the top test directory
def record_test_specs(test_dir , test_name , num_gen , gen_size, train_data_name , test_data_name , labels_data_name , eval_method , variable_mutation_rate , g_layers , g_layersize , breed_method, input_dim , output_dim):
    filename = testname + "_report.json"
    reporting.write_json(test_dir , filename , test_name=test_name , num_gen=num_gen , gen_size=gen_size , train_data_name=train_data_name , test_data_name=test_data_name ,
        eval_method=eval_method , variable_mutation_rate=variable_mutation_rate , g_layers=g_layers , g_layersize=g_layersize , breed_method=breed_method, input_dim=input_dim , output_dim=output_dim , labels_data_name=labels_data_name)

# train an individual child of a generation
def train_child(gen_folder, child_name , input_dim , output_dim , dna , training_data , test_data , labels_data):
    # setup folder
    child_folder = io.create_subfolder(gen_folder , child_name)
    # train ptsne
    perplexity , layers = G.decode_dna(dna)
    ptsne = Parametric_tSNE(input_dim , output_dim , perplexity , all_layers=layers)
    losses = ptsne.fit(training_data , verbose=False)

    # tform test data
    tform = ptsne.transform(test_data)

    # TODO ------ save if necessary the model ------------

    # free memory
    ptsne.clear_session()

    # save data
    knn_error = stats.get_knn_error(tform , labels_data)
    eval_value = evaluate()
    report_name = child_name + "_report.json"
    reporting.write_json(child_folder , report_name , child_name=child_name , input_dim=input_dim , output_dim=output_dim , perplexity=perplexity , layers=layers , loss=losses , tform=tform , knn_error=knn_error, DNA=dna)
    #produce_graphs()


if __name__ == "__main__":
    #record_test_specs(Path.cwd() , 'test1' , 10 , 20 , 'training_set.csv' , '2018-eos.csv' , 'half_auc' , False , 8 , 12 , 'layerwise')
    pass
