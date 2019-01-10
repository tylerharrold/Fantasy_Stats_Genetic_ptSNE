from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# path to put new gen reports
write_dir = Path.cwd() / "Redrawn_Plots_Curve"

data_dir = Path.cwd() / "TestData" / "MultiGenTest"

for dir in [x for x in data_dir.iterdir() if x.is_dir()]:
    for subdir in [y for y in dir.iterdir() if y.is_dir()]:
        strs = str(subdir).split('\\')
        pltname = strs[-2] + '_' + strs[-1]
        csv_file = subdir / 'loss.csv'
        csv = pd.read_csv(str(csv_file) , sep=',' , header=None)
        vals = csv.values[0]
        points = [(x,y) for x, y in enumerate(vals)]
        x = [x for x,y in points]
        y = [y for x,y in points]

        z = np.polyfit(x, y, 2)
        f = np.poly1d(z)

        x_new = np.linspace(x[0] , x[-1] , x[-1])
        y_new = f(x_new)

        plt.plot(x,y,'b.')
        plt.plot(x_new,y_new,'m-',linewidth=3)
        filename = write_dir / pltname
        plt.savefig(str(filename))
        plt.clf()
