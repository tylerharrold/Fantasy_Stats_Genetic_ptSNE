# Methods for writing reports (in json format) on models and/or generations, tests
# NOTE - this is essentially a refactor for the report_writing script

import json
from pathlib import Path
from Genetics_Refactored import Genetics
import tools

# testing tools
TEST_GEN_TGT = Path.cwd() / "TestData" / "half_curve_layer_swap_40" / "generation_30"
TEST_MODEL_TGT = TEST_GEN_TGT / "child_40"


# returns a dict of data for an individual model (i.e. a child)
def get_individual_model_report(name , dna_string , losses_list, eval_type = 'auc' , legacy_dna=False):
    report = {}
    perplexity, shape = Genetics.decode_dna(dna_string , legacy_dna=legacy_dna)
    report['dna'] = dna_string
    report['perplexity'] = perplexity
    report['shape'] = shape
    report['name'] = name
    if eval_type is 'auc':
        eval = tools.get_area_under_curve(losses_list)
    elif eval_type is 'half_auc':
        eval = tools.get_area_under_half_curve(losses_list)
    else:
        print("critical error")
    report[eval_type] = eval
    return report

# returns a dict of data for an entire training generation
def get_generation_report():
    pass

# returns a dict of data for an entire test
def get_test_report():
    pass


# targets a specific folder for an individual model and returns a dict report
def get_model_report_from_folder(folder_path):
    name = tools.get_name_from_dir_path(folder_path)
    dna_string = tools.read_dna(folder_path)
    losses_list = tools.read_loss(folder_path)
    eval_type = 'half_auc'
    legacy_dna = True
    return get_individual_model_report(name, dna_string , losses_list , eval_type, legacy_dna)
