import pandas as pd
ds=pd.read_csv('game_admin_derived.csv')
print(ds['is_attack'].value_counts(dropna=False))
print(ds['is_attack'].isnull().sum())