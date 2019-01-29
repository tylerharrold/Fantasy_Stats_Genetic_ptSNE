import pandas as pd
import numpy as np

df=pd.read_csv('2017_fantasy_data.csv', sep=',',header=0)


# fills NaN values in column with zero value
for name,item in df.iteritems():
	print(name)
	df[name] = df[name].fillna(0)

df.to_csv(path_or_buf='clean.csv' , sep=',', index=False)

