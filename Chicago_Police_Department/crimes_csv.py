'''
Author: Esther Edith Spurlock

Purpose: to examine the CPD CSV I have downloaded from:
https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present-Dashboard/5cd6-ry5g
'''

import pandas as pd
import gc

df = pd.read_csv('Crimes_-_2001_to_present.csv') #turns downloaded data into a pandas dataframe

for year in [2019, 2018, 2017, 2016]: #You can change this to include only the year(s) you want information for
    filt = df['Year'] == year #filters out only the year you want
    df_yr = df[filt]
    name = ('CPD_%s.csv' %str(year)) #creates a name specific to the year you are getting information for
    df_yr.to_csv(name) #turns the filtered dataframe into a CSV

#The following commands clean up the objects you created
del df
del filt
del name
del year
del df_yr
gc.collect
