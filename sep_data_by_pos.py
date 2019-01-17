import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


#data_dir = Path.cwd() / 'DUMMY' / 'DELETE' / 'generation_1' / 'child_1'

target_file = Path.cwd() / 'test_predic.csv'

csv = pd.read_csv(str(target_file) , sep=',' , header=None)
data = csv.values

x_vals = [x for x,y in data]
y_vals = [y for x,y in data]
#print(x_vals[0] , ',' , y_vals[0])

#lz = [x_vals, y_vals]

# for segregation, we need to creae a master list including xval, yval and labels
labels_target = Path.cwd() / 'RBMTrainingDataset' / '2018_labels.csv'
labels = pd.read_csv(str(labels_target) , sep=',' , header=None)
data_labels = labels.values
l_list = [(l,t,p) for l,t,p in data_labels]


# get a dict of all our positions
num_pos = 1
pos_dict = {}

for x,y,(name,team,pos) in zip(x_vals,y_vals,l_list):
	if pos not in pos_dict:
		pos_dict[pos] = []
		pos_dict[pos].append((x,y,name,team,pos))
	else:
		pos_dict[pos].append((x,y,name,team,pos))

#NOTE we don't really need to separate the lists we can just use the color
# dict to color the position by pos, but whatever for now

# plot each of the 
color_dict = {
	"QB":"b.",
	"RB":"g.",
	"WR":"r.",
	"0":"y.",
	"TE":"m."
}

for pos_list in pos_dict.values():
	for (x,y,name,team,pos) in pos_list:
		plt.plot(x,y, color_dict[pos])

plt.show()


'''
for x,y,label in zip(x_vals,y_vals,l_list):
	print(x , y , label)
'''


'''
plt.plot(x_vals, y_vals , 'b.')

labels_target = Path.cwd() / 'RBMTrainingDataset' / '2018_labels.csv'
labels = pd.read_csv(str(labels_target) , sep=',' , header=None)
data_labels = labels.values
l_list = [l for l,t,p in data_labels]
#print(str(lz))

for i, text in enumerate(data_labels):
    plt.annotate(str(text), (x_vals[i] , y_vals[i]))

'''




#plt.show()