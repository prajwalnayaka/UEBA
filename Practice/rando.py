import random as rd
import pandas as pd
ds=pd.read_csv('sales.csv')
print(ds['Outcome'].value_counts(normalize=True).mul(100).round(1).astype(str)+'%')