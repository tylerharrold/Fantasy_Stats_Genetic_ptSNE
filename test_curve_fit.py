from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

write_dir = Path.cwd()

data_file = Path.cwd() / "TestData" / "MultiGenTest" / "generation_1" / 'child_1' / 'loss.csv'

csv = pd.read_csv(str(data_file) , sep=',' , header=None)
vals = csv.values[0]

points = [(x,y) for x, y in enumerate(vals)]
x = [x for x,y in points]
y = [y for x,y in points]

z = np.polyfit(x, y, 2)
f = np.poly1d(z)
f_prime = np.polyint(f)



x_new = np.linspace(x[0] , x[-1] , x[-1])
y_new = f(x_new)

print("f =")
print(f)
print("The integral of f= ")
print(np.polyint(f))

print("lets do math")
print(f_prime(x[0]))
print(f_prime(x[-1]))


#plt.plot(x,y,'b.',x_new,y_new)
#plt.xlim(x[0]-1,x[-1]+1)
'''
plt.plot(x,y,'b.')
plt.plot(x_new,y_new,'m-',linewidth=3)
plt.show()
'''
