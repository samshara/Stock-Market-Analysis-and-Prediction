import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sys import argv
#import indicators

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
prev = 0
signal = []
for value in df20[' Close Price']:
    if(value>prev):
        signal.append('up')
    else:
        signal.append('down')
    # else:
    #     signal.append('flat')
    prev = value
# plt.plot(df10, label = 'window=10')
# plt.plot(df20, label = 'window=20')
# plt.show()
## Display the plot
#plt.show()                      
# calculate difference
# diff = df20 - df10
# signal = []
# c = 1
# for value in diff[' Close Price']:
#     if value > 0 and c == -1:
#         signal.append('2')  # sell
#         c = 1
#     elif value < 0 and c == 1:
#         signal.append('1') # buy
#         c = -1
#     else:
#         signal.append('0') # hold
# # signal = pd.DataFrame(signal)
#nabil['ma20'] = df20[' Close Price']
nabil['signal'] = signal
# print(nabil.madiff)
nabil.to_csv('../../data/signal_trend.csv',encoding = 'utf-8')
