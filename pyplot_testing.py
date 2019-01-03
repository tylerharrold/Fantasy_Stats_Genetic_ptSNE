import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


data_dir = Path.cwd() / 'DUMMY' / 'DELETE' / 'generation_1' / 'child_1'

target_file = data_dir / 'loss.csv'

csv = pd.read_csv(str(target_file) , sep=',' , header=None)
vals = csv.values[0]

'''
for i,j in [(x+1,y) for (x,y) in enumerate(vals)]:
    print(i)
'''


print(vals)
plt.plot(vals , 'b.')
plt.ylabel('loss')
plt.savefig('testplt.png')
plt.show()
