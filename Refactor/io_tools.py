from pathlib import Path
import os
import pandas as pd


def b_directory_exists(working_directory , target_directory_name):
    return target_directory_name in [f.name for f in working_directory.iterdir() if f.is_dir()]

# creates a directory of new_name in specified target_directory
def create_directory(target_directory , new_name):
    os.mkdir(str(target_directory / new_name))

# creates a subfolder and returns the path to it
def create_subfolder(directory , sub_name):
    create_directory(directory , sub_name)
    return (directory / sub_name)

# write data to csv
def write_csv(target_dir , data , filename):
    df = pd.DataFrame(data)
    df.to_csv(path_or_buf=str(target_dir / filename) , sep=',' , index=False , header=None)
