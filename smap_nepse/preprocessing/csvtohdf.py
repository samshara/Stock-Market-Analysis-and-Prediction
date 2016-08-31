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
        data = pd.read_csv(source,index_col = 0,parse_dates=True, encoding = "ISO-8859-1")
    except(FileNotFoundError, IOError):
        print('Wrong file or file path.')
        return
    if data.empty:
        return

    data.to_hdf(destination, 'data', mode='w', format='table')
    return

def alltohdf(source, destination='../../hdf/'):
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

def build_hdfstore(source_dir, destination='../../hdf/store.h5'):
    """ Creates a hdf5 store of all the csv files present in the source directory.
    The hdf5 store is placed in the destination path.
    param:
          source_dir: The source directory containing the csv files.
          destination: The path for the hdf5 store.
    returns:
          destination: The path for the hdf5 store.
"""

    # Delete destination file if it exists. If destination is not deleted the
    # hdf contents are appended to the file which causes data consistency problems.
    try:
        os.remove(destination)
    except OSError:
        pass

    os.makedirs(os.path.dirname(destination), exist_ok=True)

    os.chdir(source_dir)
    for file in glob.glob("*.csv"):
        print('Appending {}.csv to hdfstore...\n'.format(file))
        try:
            data = pd.read_csv(file,index_col = 0,parse_dates=True)
        except(FileNotFoundError, IOError):
            print('Wrong file or file path.')
            return
        data.to_hdf(destination, file.strip('.csv') , mode='a', format='fixed')
    return destination

if __name__ == '__main__':
    build_hdfstore('../../data/','../../hdf/store.h5')
