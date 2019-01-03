# functions for evaluating generations of trained neural networks
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# target path
csv_path = Path.cwd() / 'TestData' / 'MultiGenTest' / 'generation_5' / 'child_10' / 'loss.csv'

csv = pd.read_csv(str(csv_path) , sep=',' , header=None)
vals = csv.values[0]
print(len(vals))
plt.plot(vals , 'b.')
plt.ylabel('loss')
filename = Path.cwd() / 'gen10plot.png'
plt.savefig(str(filename))
