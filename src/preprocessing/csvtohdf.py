import pandas as pd
import numpy as np
import os
import glob

def csvtohdf(source, destination):
    """Takes a csv file as input and storest it as a hdf5 file in the
    destnation path.
    The hdf5 file is stored in table format.
"""
    try:
        data = pd.read_csv(source,index_col = 0,parse_dates=True)
    except(FileNotFoundError, IOError):
        print('Wrong file or file path.')
        return
    if data.empty:
        return

    data.to_hdf(destination, 'data', mode='w', format='table')
    return

def alltohdf(source, destination='../hdf/'):
    """Performs storing of all .csv file present on source directory in a hdf5
    data format and save in destination folder."""

    if not os.path.exists(destination):
        os.makedirs(destination)

    os.chdir(source)
    for file in glob.glob("*.csv"):
        filename = os.path.basename(file)
        print('Saving {}...\n'.format(filename))
        csvtohdf(file, destination+filename)
    return
