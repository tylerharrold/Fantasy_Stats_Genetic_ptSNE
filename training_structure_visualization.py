from pathlib import Path
from Genetics import Genetics
from tools import read_dna

# custom function for sorting the folders in a generation corrected
def sort_genfolders(folderpath):
    folderstring = folderpath.name
    _ , num = folderstring.split('_')
    return int(num)

# for a given strand of DNA, pretty print the structure
def unpack_dna(dna , genetic_helper):
    return genetic_helper.decode_dna(dna)

# for a generation, sort the structures of the dna
def organize_structures(gen_dir):
    children = []
    genetic_helper = Genetics()
    for child in [x for x in gen_dir.iterdir() if x.is_dir()]:
        name = child.name
        dna = read_dna(child)
        perplexity, structure = unpack_dna(dna , genetic_helper)
        children.append([name, perplexity, structure , dna])

    # sort the list
    children.sort(key=lambda x : x[2])

    for name, perplexity, structure,  _ in children:
        print(name , ':' , perplexity , ':     ' , structure)

def package_child_data(childpath , genetic_helper):
    name = childpath.name
    dna = read_dna(childpath)
    perplexity, structure = unpack_dna(dna , genetic_helper)
    return [name , perplexity , structure , dna]

def package_generation_data(genpath , genetic_helper):
    children = []
    for child in [dir for dir in genpath.iterdir() if dir.is_dir()]:
        child_data = package_child_data(child , genetic_helper)
        children.append(child_data)

    #sort the children by their structure list
    children = sorted(children , key=lambda x:x[2])
    return children

def mark_child_as_previous_best_performer(child_data_list , list_of_prev_generation_children):
    child_dna = child_data_list[3]
    previous_gene_pool = [child[3] for child in list_of_prev_generation_children]
    # if the dna of the child in question can be found in the previous gen's gene, pool, mark it with an asterix
    if child_dna in previous_gene_pool:
        child_data_list[0] = child_data_list[0] + '*****'

# for a test, iterate through each generation and print out results
def get_test_structure_report(test_dir):
    genetic_helper = genetic_helper = Genetics()
    # get a properly organized list of child generation paths
    genfolders = [dir for dir in test_dir.iterdir() if dir.is_dir()]
    sorted_genfolders = sorted(genfolders , key=sort_genfolders)
    # get all generational data
    generations = []
    for generation in sorted_genfolders:
        generations.append(package_generation_data(generation , genetic_helper))

    # for all generations (other than first) mark the children who survived from previous generations
    for previous_gen, current_gen in zip(generations , generations[1:]):
        # need to see which of the children were present in prevous generation
        for child in current_gen:
            mark_child_as_previous_best_performer(child , previous_gen)

    return generations

# writes out full report on the genetic structures of test generations
def save_test_structure_report(test_dir , save_dir , save_name):
    generations = get_test_structure_report(test_dir)
    with (save_dir / save_name).open('w') as file:
        for gen_number , generation in enumerate(generations , start=1):
            file.write("GENERATION " + str(gen_number) +'\n\n')
            for child in generation:
                file.write(child[0].ljust(8,' ') + ': ' + str(child[1]).ljust(2 , ' ') + ': ' + str(child[2]) + '\n')
            # after a generation has printed, skip one line
            file.write('\n')

# writes out a file just observing the lineage of best performers
def save_test_best_performers(test_dir , save_dir , save_name):
    generations = get_test_structure_report(test_dir)
    with (save_dir / save_name).open('w') as file:
        for gen_number , generation in enumerate(generations , start=1):
            file.write("GENERATION " + str(gen_number) +'\n')
            for child in generation:
                if '*' in child[0]:
                    file.write(child[0].ljust(8,' ') + ': ' + str(child[1]).ljust(2 , ' ') + ': ' + str(child[2]) + '\n')
            # after a generation has printed, skip one line
            file.write('\n')



if __name__ == "__main__":
    test_names = ['normalized_combine_3D_30_40_half_auc' ,
                'normalized_combine_30_40_half_auc' ,
                'normalized_fantasy_3D_30_40_half_auc' ,
                'normalized_fantasy_30_40_half_auc'
    ]

    test_dir = Path.cwd() / "TestData"
    for name in test_names:
        print("saving data for: " , str(test_dir / name))
        save_test_structure_report((test_dir / name) , (test_dir / name) , 'structure_report.txt')
        save_test_best_performers((test_dir / name) , (test_dir / name) , 'surviving_lineage.txt')
