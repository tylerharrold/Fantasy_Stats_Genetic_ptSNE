import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd


graphing_target = Path.cwd() / 'test_predic.csv'
csv = pd.read_csv(str(graphing_target) , sep=',' , header=None)
data = csv.values


x_vals = [x for x,y in data]
y_vals = [y for x,y in data]
print(x_vals[0] , ',' , y_vals[0])

lz = [x_vals, y_vals]

#plt.plot(tups , 'b.')


#plt.plot(x_vals, y_vals , 'b.')

#plt.ylabel('loss')

plt.plot(x_vals, y_vals , 'b.')

#plt.plot(tups, 'r.')



labels_target = Path.cwd() / 'RBMTrainingDataset' / '2018_labels.csv'
labels = pd.read_csv(str(labels_target) , sep=',' , header=None)
data_labels = labels.values
l_list = [l for l,t,p in data_labels]
#print(str(lz))

for i, text in enumerate(data_labels):
    plt.annotate(str(text), (x_vals[i] , y_vals[i]))




plt.show()
#plt.savefig(str(Path.cwd() / 'tups'))
