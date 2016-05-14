import pandas as pd
import numpy as np
import os
import glob

def cleancsv(source, destination):
    """Removes duplicates,forward fills the missing values based on date attribute
    from the source data and saves it to destination path."""

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
    return

def cleanall(source, destination='../cleaneddata/'):
    """Performs data cleaning on all .csv files present on the source directory and
    saves each file in destination folder."""

    if not os.path.exists(destination):
        os.makedirs(destination)

    os.chdir(source)
    for file in glob.glob("*.csv"):
        filename = os.path.basename(file)
        print('Cleaning'+filename+'...\n')
        cleancsv(file, destination+filename)
    return

cleanall('../data')
