from pathlib import Path
import pandas as pd



# exclude names

# get the target dir name
target_file = Path.cwd().parent / "NFL_Combine_Data" / '2019Both.csv'

df = pd.read_csv(str(target_file) , sep=',')

# turn all NaN values into zeros
for name,item in df.iteritems():
    df[name] = df[name].fillna(0)


# list of items to exclude
# Player,Pos,School,College,Ht,Wt,40yd,Vertical,Bench,Broad Jump,3Cone,Shuttle,Drafted (tm/rnd/yr)
include_columns = ['Ht','Wt','40yd','Vertical','Bench','Broad Jump','3Cone','Shuttle']
formatted_data = df[include_columns]

# turn the odd height value into a workable number (float)
formatted_data['Ht'] = formatted_data['Ht'].apply(lambda x : float(x.replace('-' , '.')))

save_dir = Path.cwd().parent / "Formatted_Combine_Data"

formatted_data.to_csv(str(save_dir / "2019_combine_formatted.csv") , sep=',', index=False, header=None)
