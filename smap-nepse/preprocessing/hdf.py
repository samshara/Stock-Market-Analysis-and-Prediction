import pandas as pd
import numpy as np

#TODO: create module for creating and updating hdf store

## to enable put/append/to_hdf by default store in the table format 
pd.set_option('io.hdf.default_format','table')
# define hdf store
stockStore = pd.HDFStore('store.h5',complevel=9,complib='blosc')
# get list of stocknames
with open('../Data_Cleaner/stockname.txt') as f:
    stocknames = [line.rstrip('\n') for line in f]

for stockname in stocknames:
    csvdata = stockname + '.csv'
    ## read dataframe from csvdata
    try:
        df =  pd.read_csv('Stock_Data_Cleaned/'+csvdata, index_col = 0, parse_dates = True)
        stockStore[stockname] = df
    except Exception as e:
        print(stockname + " unable to create dataframe\n" +str(e))

# stockStore.append('ACEDBL',df1)
print(stockStore)

#print(stockStore.keys())
stockStore.close()
