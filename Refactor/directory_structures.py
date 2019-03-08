from pathlib import Path
import os


def b_directory_exists(working_directory , target_directory_name):
    return target_directory_name in [f.name for f in working_directory.iterdir() if f.is_dir()]

# creates a directory of new_name in specified target_directory
def create_directory(target_directory , new_name):
    os.mkdir(str(target_directory / new_name))
