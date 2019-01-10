from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# path to put new gen reports
write_dir = Path.cwd() / "Redrawn_Plots"

data_dir = Path.cwd() / "TestData" / "MultiGenTest"

for dir in [x for x in data_dir.iterdir() if x.is_dir()]:
    for subdir in [y for y in dir.iterdir() if y.is_dir()]:
        strs = str(subdir).split('\\')
        pltname = strs[-2] + '_' + strs[-1]
        csv_file = subdir / 'loss.csv'
        csv = pd.read_csv(str(csv_file) , sep=',' , header=None)
        vals = csv.values[0]
        plt.plot(vals, 'b.')
        plt.ylabel('loss')
        filename = write_dir / pltname
        plt.savefig(str(filename))
        plt.clf()
