# a set of tools to write reports on the models being trained, the generations they were trained in
# and the overall test that was conducted
import json
from tools import setup_file_structure
from pathlib import Path
import os
from Genetics import Genetics
import tools

# given a testing directory, record the input dims and the output dims for the test
def log_basic_test_params(dir, test_name , num_generations, generation_size, input_dims, output_dims, max_layers, bits_per_layer, evaluation_type):
    data = {}
    data['test_name'] = test_name
    data['num_generations'] = num_generations
    data['generation_size'] = generation_size
    data['input_dims'] = input_dims
    data['output_dims'] = output_dims
    data['max_layers'] = max_layers
    data['bits_per_layer'] = bits_per_layer
    data['evaluation_type'] = evaluation_type

    with open(str(dir / 'params.json') , 'w') as outfile:
        json.dump(data, outfile)

# given a generation directory, current mutation rate
def record_mutation_rate(generation_name, mutation_rate):
    pass

# save report for generation using the area under curve evaluation
def write_generation_report_auc(generation_dir , write_dir):
    data = {}
    data['children'] = []
    for child in [c for c in generation_dir.iterdir() if c.is_dir()]:
        child_write_dir = write_dir / (child.name + "_report")
        os.mkdir(str(child_write_dir))
        child_data = get_child_report_auc(child , child_write_dir)
        data['children'].append(child_data)
    # write the whole gen
    with open(str(write_dir / 'gen_report.json') , 'w') as outfile:
        json.dump(data , outfile)

# given child record the dna, performance of each child in generation (using auc), the perplexity, and the shape
def get_child_report_auc(child_dir , write_dir, dna_max_layers=8 , dna_bits_per_layer=12, write=True):
    g = Genetics(dna_max_layers , dna_bits_per_layer)
    report = {}
    dna = tools.read_dna(child_dir)
    perplexity, shape = g.decode_dna(dna)
    report['dna'] = dna
    report['perplexity'] = perplexity
    report['shape'] = shape
    report['name'] = child_dir.name
    loss = tools.read_loss(child_dir)
    auc = tools.get_area_under_curve(loss)
    report['area_under_curve'] = auc

    if write:
        with open(str(write_dir / 'report.json') , 'w') as outfile:
            json.dump(report, outfile)

    return report


# given a child record the dna, performance of each child in generation (using variance) , the perplexity, and the shape

# given a child record the dna, performance of each child in generation (using linear) , the perplexity, and the shape

# given a child record the dna, performance of each child in generation (using vector) , the perplexity, and the shape

# for a test, record the best performers for each generation, with option to automatically save for each generation individually
# method for full sweep analysis of a test directory that saves reporting in one place
def analyze_test(test_dir, report_dir):
    active_dir = Path.cwd()
    if (active_dir / report_dir) not in [x for x in active_dir.iterdir() if x.is_dir()]:
        os.mkdir(str(active_dir / report_dir))
        report_dir = active_dir / report_dir
    else:
        print("Specified report directory already exists...quitting...")
        quit()
    for generation in [x for x in test_dir.iterdir() if x.is_dir()]:
        gen_report_dir = report_dir / (generation.name + "_report")
        os.mkdir(str(gen_report_dir))
        write_generation_report_auc(generation , gen_report_dir)
