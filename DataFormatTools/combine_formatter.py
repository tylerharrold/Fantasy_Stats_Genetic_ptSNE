from pathlib import Path
import pandas as pd


# import
'''
# fills NaN values in column with zero value
for name,item in df.iteritems():
	print(name)
	df[name] = df[name].fillna(0)
    '''

#newdf = initialdf.append(theappendingdf)

# exclude names

# get the target dir name
target_dir = Path.cwd().parent / "NFL_Combine_Data"

#create an empty df
combined_list = pd.DataFrame()

#iterate through all csvs in directory and append the imported results to the combined list
for file in target_dir.iterdir():
    df = pd.read_csv(str(file) , sep=',')
    combined_list = combined_list.append(df)

# turn all NaN values into zeros
for name,item in combined_list.iteritems():
    combined_list[name] = combined_list[name].fillna(0)


# list of items to exclude
# Rk,Year,Player,Pos,AV,School,College,Height,Wt,40YD,Vertical,BenchReps,Broad Jump,3Cone,Shuttle,Drafted (tm/rnd/yr)
include_columns = ['Height','Wt','40YD','Vertical','BenchReps','Broad Jump','3Cone','Shuttle']
formatted_data = combined_list[include_columns]

# turn the odd height value into a workable number (float)
formatted_data['Height'] = formatted_data['Height'].apply(lambda x : float(x.replace('-' , '.')))

save_dir = Path.cwd().parent / "Formatted_Combine_Data"

formatted_data.to_csv(str(save_dir / "combine_formatted.csv") , sep=',', index=False, header=None)
