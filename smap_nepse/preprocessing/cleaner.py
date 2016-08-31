#cleaner.py
#! /usr/bin/env python3
"""
Provides methods to clean raw .csv files.

This module provides functions to clean single .csv files or all .csv files
present in a given floder. The cleaned .csv files are saved at destination path.

Available functions:
 -cleancsv: Clean a single .csv file and store it.
 -cleanall: Clean all .csv files present in a directory and store it.
"""
import pandas as pd
import numpy as np
import os
import glob
import csv

from indicator import RSI,movingaverage,macd

def cleancsv(source, destination):
    """Removes duplicates,forward fills the missing values based on date attribute
    from the source data and saves it to destination path.
    Arguments:
        source: pathname of the sourcefile
        destination: pathname for the cleaned data.
"""

    try:
        data = pd.read_csv(source,parse_dates=True)
    except (FileNotFoundError, IOError):
        print('Wrong file or file path.')
        return
    if data.empty:
        return

    data  = data.drop_duplicates(subset = 'Date', keep='first')

    data = data.set_index(pd.DatetimeIndex(data.Date))

    idx = pd.date_range(data.index.min(), data.index.max())
    indexed_data = data.reindex(index = idx, fill_value = np.nan)
    indexed_data = indexed_data.replace('0', np.nan)
    indexed_data = indexed_data.fillna(method='ffill')
    indexed_data = indexed_data.drop('Date', 1)

    indexed_data.to_csv(destination, index_label='Date')


def cleanall(source, destination='../../cleaneddata/'):
    """Performs data cleaning on all .csv files present on the source directory
    and saves each file in destination folder.
    Arguments:
        source: source directory containing raw data.
        destination: destination directory to store cleaned data.
"""

    if not os.path.exists(destination):
        os.makedirs(destination)

    os.chdir(source)
    for file in glob.glob("*.csv"):
        filename = os.path.basename(file)
        print('Cleaning'+filename+'...\n')
        cleancsv(file, destination+filename)

def calcopening(source):
    try:
        data = pd.read_csv(source,index_col = 0,parse_dates=True)
    except (FileNotFoundError, IOError):
        print('Wrong file or file path.')
        return
    if data.empty:
        return

    data['Opening Price'] = data['Closing Price'].shift(1)
    # The Opening Price must be adjusted so that it is smaller than Maximum Price
    # and larger than Minimum Price
    data['Maximum Price'] = data[['Opening Price', 'Maximum Price', 'Minimum Price', 'Closing Price']].max(axis=1)
    data['Minimum Price'] = data[['Opening Price', 'Maximum Price', 'Minimum Price', 'Closing Price']].min(axis=1)
    data.set_value(data.index[0],'Opening Price', data.get_value(data.index[0],'Closing Price'))
    data.to_csv(source,index=True)

def addindicators(source):
    try:
        data = pd.read_csv(source,index_col = 0,parse_dates=True)
    except (FileNotFoundError, IOError):
        print('Wrong file or file path.')
        return
    if data.empty:
        return

    data = RSI(data)
    data = movingaverage(data)
    data = macd(data)
    data =data.round(5)
    data.to_csv(source,index=True)

def applyfunc(func,source,*args,**kwargs):
    os.chdir(source)
    for file in glob.glob("*.csv"):
        filename = os.path.basename(file)
        func(file,*args,**kwargs)

if __name__ == "__main__":
    cleanall('../../data/')
    applyfunc(calcopening,'../../cleaneddata/')
    applyfunc(addindicators,'../../cleaneddata/')
