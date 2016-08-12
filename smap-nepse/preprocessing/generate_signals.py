import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sys import argv

__author__ = "Semanta Bhandari"
__copyright__ = ""
__credits__ = ["Sameer Rai","Sumit Shrestha","Sankalpa Timilsina"]
__license__ = ""
__version__ = "0.1"
__email__ = "semantabhandari@gmail.com"

def signal_updown(dataframe, window):
    '''
    Generate 'up' or 'down' signal as target for analysis
    
    Parameters:
    dataframe: dataframe of data whose signal is to be generated
    window: signal for n number of days ahead
    filename: name of csv file to save data

    Returns: dataframe with signal
    '''
    signal = []
    values = dataframe[' Close Price'].values
    for i in range(0,len(values)-window):
        if(values[i+window]>values[i]):
            signal.append('up')
        else:
            signal.append('down')
    signal.append('up')
    dataframe['signal'] = signal
    return dataframe

dataframe = pd.read_csv('../../data/Stock_Data_Cleaned/NABIL.csv', index_col=0, parse_dates=True)
print(dataframe[:10])
df = signal_updown(dataframe, 1)
print(df[:10])
