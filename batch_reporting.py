from pathlib import Path
from statistical_reporting import half_auc_error_reports
from statistical_reporting import knn_error_reports
from statistical_reporting import gen_stats_half_auc
from statistical_reporting import gen_stats_knn
from statistical_tools import get_knn_error
from tools import get_ndarray
import json



# get the path the the testing directory
def batch_report(test_dir , eval_type='half_auc'):
    # iterate through all subfolders and get evaluation reports based on eval_type
    if eval_type is 'half_auc':
        half_auc_error_reports(test_dir)
        gen_stats_half_auc(test_dir)
    elif eval_type is 'knn_error':
        knn_error_reports(test_dir)
        gen_stats_knn(test_dir)

def analyze_performance_knn(generation_dir  , labels_path):
    data = {}
    for child_dir in [x for x in generation_dir.iterdir() if x.is_dir()]:
        name = child_dir.name
        tform = get_ndarray(str(child_dir / "tform.csv"))
        labels = get_ndarray(str(labels_path))
        knn_error = get_knn_error(tform , labels)
        data[name] = {'knn_error':knn_error}
    with open(str(generation_dir / 'knn_eval.json') , 'w') as outfile:
        json.dump(data, outfile)
