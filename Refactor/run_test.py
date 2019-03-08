# file containing master function that accepts areguments to runa multi
# generational ptsne training
import directory_structures as dir_struct
import reporting
from pathlib import Path
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
def train(testname , num_gen, gen_size, train_data , train_data_name , test_data , test_data_name , output_dim, eval_method, write_directory, g_layers, g_layersize , g_mutation_rate,  breed_method="layerwise" , save_model=False , variable_mutation_rate=False):
    # setup directory in write_directory with the name of the test
    test_dir = setup_file_struct(write_directory , testname)
    # within this directory, record the basic specs
    record_test_specs(test_dir , testname , num_gen, gen_size , train_data_name , test_data_name , eval_method , variable_mutation_rate , g_layers, g_layersize, breed_method)

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

    pass

# sets up file structure, returns the test's directory path
def setup_file_struct(write_directory , testname):
    if dir_struct.b_directory_exists(write_directory , testname):
        print("directory already exists, quitting to avoid overwrite")
        quit()
    else:
        dir_struct.create_directory(write_directory , testname)
        return (write_directory / testname)

# records the test specs in the top test directory
def record_test_specs(test_dir , testname , num_gen , gen_size, train_data_name , test_data_name , eval_method , variable_mutation_rate , g_layers , g_layersize , breed_method):
    filename = testname + "_report.json"
    reporting.write_json(test_dir , filename , test_name=testname , num_gen=num_gen , gen_size=gen_size , train_data_name=train_data_name , test_data_name=test_data_name ,
        eval_method=eval_method , variable_mutation_rate=variable_mutation_rate , g_layers=g_layers , g_layersize=g_layersize , breed_method=breed_method)


if __name__ == "__main__":
    #record_test_specs(Path.cwd() , 'test1' , 10 , 20 , 'training_set.csv' , '2018-eos.csv' , 'half_auc' , False , 8 , 12 , 'layerwise')
    pass
