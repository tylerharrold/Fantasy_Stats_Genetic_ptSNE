import json
import math
from pathlib import Path

def get_generation_mean(json_data):
    data = json_data['children']
    len_data = len(data)
    mean = 0
    for d in data:
        mean = mean + d['area_under_curve']
    mean = mean / len_data
    return mean

def get_generation_variance(json_data , sample_mean):
    sigma = 0
    data = json_data['children']
    n = len(data)
    for d in data:
        sigma = sigma + (d['area_under_curve'] - sample_mean)**2
    variance = sigma / (n - 1)
    return variance

def get_generation_stddev(gen_variance):
    return math.sqrt(gen_variance)


def print_stats(json):
    mean = get_generation_mean(json)
    variance = get_generation_variance(json, mean)
    stddev = get_generation_stddev(variance)
    print('mean: ' , mean)
    print('var: ' , variance)
    print('stddev: ' , stddev)



if __name__ == "__main__":
    report = Path.cwd() / "Reports" / "HC_LS_G30_N40_Report" / "generation_30_report" / "gen_report.json"
    with open(str(report)) as jsonfile:
        data = json.load(jsonfile)
    print_stats(data)
