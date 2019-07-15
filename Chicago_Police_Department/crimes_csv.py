'''
Author: Esther Edith Spurlock

Purpose: to examine the CPD CSV I have downloaded from:
https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present-Dashboard/5cd6-ry5g
'''

import pandas as pd
import gc

df = pd.read_csv('Crimes_-_2001_to_present.csv')
print(df.columns)
for year in [2019, 2018, 2017, 2016]:
    print(year)
    filt = df['Year'] == year
    df_yr = df[filt]
    print(df_yr.shape)
    name = ('CPD_%s.csv' %str(year))
    df_yr.to_csv(name)
    df_yr.dropna(subset=['Block'], inplace=True)
    print(df_yr.shape)

del df
del filt
del name
del year
del df_yr
gc.collect
print('Complete')

#112,910 with NAs (2019)
#90,651 (80.3% of total data) without NAs in Lat and Long (2019)

#267,028 with NAs (2018)
#263,458 (98.7% of total data) without NAs in Lat and Long (2018)
