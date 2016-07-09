import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sys import argv
#import indicators
#TODO: create module for generating stock signal 

## to enable put/append/to_hdf by default store in the table format 
pd.set_option('io.hdf.default_format','table')
# define hdf store
stockStore = pd.HDFStore('../../data/store.h5',complevel=9,complib='blosc')
nabil = stockStore.NABIL
plt.figure()
#plt.plot(nabil[' Close Price'])
#calculating moving avarage
data_mean10 = pd.rolling_mean(nabil[' Close Price'],window=10)
data_mean20 = pd.rolling_mean(nabil[' Close Price'],window=20)
df10 = pd.DataFrame(data_mean10)
df20 = pd.DataFrame(data_mean20)
signal = []
values = df20[' Close Price'].values
for i in range(0,len(values)-1):
    if(values[i+1]>values[i]):
        signal.append('up')
    else:
        signal.append('down')
signal.append('up')
# plt.plot(df10, label = 'window=10')
# plt.plot(df20, label = 'window=20')
# plt.show()
## Display the plot
#plt.show()                      
# calculate difference
# diff = df20 - df10

nabil['signal'] = signal
nabil.to_csv('../../data/sample_trend.csv',encoding = 'utf-8')
