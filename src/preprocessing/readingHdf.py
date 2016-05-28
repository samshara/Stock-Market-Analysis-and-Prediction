import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## to enable put/append/to_hdf by default store in the table format 
pd.set_option('io.hdf.default_format','table')
# define hdf store
stockStore = pd.HDFStore('store.h5',complevel=9,complib='blosc')

nabil = stockStore.NABIL
unl = stockStore.UNL
sanima = stockStore.SANIMA
uic  = stockStore.UIC
nbb = stockStore.NBB


# sth = pd.read_hdf('store.h5','NABIL',where="index='2014-04-15'")
# sth2 = pd.read_hdf('store.h5','SANIMA',where="index='2014-04-15'")

# print(sth)
# print(sth2)

## To plot
nabil[' Close Price'].plot(title = 'cleaned',label = 'NABIL',linestyle=':')
#unl[' Close Price'].plot(label = 'UNL')
uic[' Close Price'].plot(label = 'UIC')
sanima[' Close Price'].plot(label = 'SANIMA',linestyle='--')
nbb[' Close Price'].plot(label = 'NBB',linestyle='-.')

plt.legend(loc=2,borderaxespad=0.)
## Display the plot 
plt.show()

stockStore.close()
