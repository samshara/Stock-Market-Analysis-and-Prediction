import pandas as pd
from sklearn import preprocessing
from pybrain.datasets import ClassificationDataSet

__author__ = "Semanta Bhandari"
__copyright__ = ""
__credits__ = ["Sameer Rai","Sumit Shrestha","Sankalpa Timilsina"]
__license__ = ""
__version__ = "0.1"
__email__ = "semantabhandari@gmail.com"

# to enable put/append/to_hdf by default store in the table format
#pd.set_option('io.hdf.default_format', 'table')


def load_hdf(filename):
    '''load hdf store from file.

    Parameters:
    filename: name of the file of hdfstore
    
    Returns: 
    stockStore: pandas hdfstore(pytable)
    '''
    stockStore = pd.HDFStore(
        '../../data/' + filename,
        complevel=9,
        complib='blosc')
    return stockStore


def load_data_frame(filename):
    '''load dataframe from csv file
    
    Parameters:
    filename: name of the csv file
    
    Returns: 
    dataframe: pandas dataframe
    '''
    dataframe = pd.read_csv(
        filename,
        index_col=0,
        parse_dates=True)
    return dataframe

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
    values = dataframe['Closing Price'].values
    data_mean20 = pd.rolling_mean(dataframe['Closing Price'],window=20)
    values = data_mean20
    for i in range(0,len(values)-window):
        if(values[i+window]>values[i]):
            signal.append('up')
        else:
            signal.append('down')
    for i in range(window):
        signal.append('NaN')
    dataframe['signal'] = signal
    return dataframe

def normalize_dataset(dataframe):
    ''' normalization of datasets'''
    __ = True


def prepare_datasets(inp, out, dataframe, ratio):
    '''conversion from pandas dataframe to ClassificationDataSet of numpy
    Parameters:
    inp: list of names of input features
    out: list of names of output features(target value)
    dataframe: dataframe of the stock data
    ratio: ratio of dimension of test to train dataset

    Returns: 
    alldata: dataset for supervised classification
    trndata: training dataset
    tstdata: testing dataset
    '''
    inp_dim = len(inp)
    out_dim = len(out)
    no_classes = 2
    alldata = ClassificationDataSet(inp_dim, out_dim, no_classes)
    inp = dataframe[inp]
    out = dataframe[out]
    # for [a,b,c],d in zip(inp.values,out.values):
    for i in range(len(inp.values)):
        d = out.values[i]
        if d == 'up':
            d = 0
        else:# d == 'down':
            d = 1
        # else:
        #     d = 2
        alldata.addSample(inp.values[i], d)
    alldata._convertToOneOfMany(bounds=[0,1])
    tstdata, trndata = alldata.splitWithProportion(ratio)
    tstdata_temp, trndata_temp = alldata.splitWithProportion(ratio)
    # to convert supervised datasets to classification datasets
    # tstdata = trndata = ClassificationDataSet(inp_dim, out_dim, no_classes)
    # for n in range(0, tstdata_temp.getLength()):
    #     tstdata.addSample(
    #         tstdata_temp.getSample(n)[0],
    #         tstdata_temp.getSample(n)[1])
    # for n in range(0, trndata_temp.getLength()):
    #     trndata.addSample(
    #         trndata_temp.getSample(n)[0],
    #         trndata_temp.getSample(n)[1])
    # trndata._convertToOneOfMany()
    # tstdata._convertToOneOfMany()
    return alldata, trndata, tstdata

if __name__== '__main__':
    #hdfStore = load_hdf('store.h5')
    #print(hdfStore)
    dataframe = load_data_frame('NABIL.csv')
    print(signal_updown(dataframe, 1)[:10])
