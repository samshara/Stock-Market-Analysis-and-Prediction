import pandas as pd
import numpy as np

## to enable put/append/to_hdf by default store in the table format 
pd.set_option('io.hdf.default_format','table')

stockStore = pd.HDFStore('../../data/h5store/store.h5')

string1 = ''
string1 += 'Stock,Start_date,End_date,no_of_data\n'
for key in stockStore.keys():
    df = stockStore[key]
    print(key)
    length = df.index.size
    if(length == 0):
        print('no data')
    else:
        start_date = str(df.index[0].date())
        end_date = str(df.index[-1].date())
        temp = key[1:]+','+start_date+','+end_date+','+str(length)+'\n'
        string1 += temp
print(string1)
fp = open('infohdf.csv','w')
fp.write(string1)
fp.close()
stockStore.close()
