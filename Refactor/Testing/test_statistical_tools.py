# file testing behavior of our statistical tool functions
from pathlib import Path
import pandas as pd
import sys
parent_dir = str(Path.cwd().parent)
sys.path.append(parent_dir)

import unittest
import statistical_tools as st

tform_data_path = Path.cwd() / "TrainingTestFolder" / "RefactoredTest" / "generation_0" / "generation_0_child_1" / "tform.csv"
data = pd.read_csv(str(tform_data_path)  , sep=',' , header=None).values
labels_data_path = Path.cwd() / "Testing_Data" / "labels.csv"
labels = pd.read_csv(str(labels_data_path) , sep=',' , header=None)[1].values

class TestDirectoryStructures(unittest.TestCase):
    def test_knn_error(self):
        print(st.get_knn_error(data , labels))

    def test_return_type(self):
        print(data)
        knn = st.get_knn_error(data , labels)
        self.assertTrue(isinstance(knn , float))



if __name__ == '__main__':
    unittest.main()
