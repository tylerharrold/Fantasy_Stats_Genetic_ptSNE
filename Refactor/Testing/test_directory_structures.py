# file testing behavior of our Genetics class
from pathlib import Path
import sys
parent_dir = str(Path.cwd().parent)
sys.path.append(parent_dir)

import unittest
import  directory_structures as d

class TestDirectoryStructures(unittest.TestCase):

    def test_b_directory_exists(self):
        testPath = Path.cwd().parent
        self.assertTrue(d.b_directory_exists(testPath , Path.cwd().name))
