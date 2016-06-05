import pandas as pd
from sklearn import preprocessing
from pybrain.datasets import ClassificationDataSet

## to enable put/append/to_hdf by default store in the table format 
pd.set_option('io.hdf.default_format','table')

def load_hdf(filename):
    '''load hdf store. Parameter: hdfstore filename'''
    stockStore = pd.HDFStore('../../data/'+filename,complevel=9,complib='blosc')
    return stockStore
    
def load_data_frame(filename):
    dataframe = pd.read_csv('../../data/'+filename, index_col = 0, parse_dates = True)
    return dataframe

    
def normalize_dataset(dataframe):
    __ = True


def prepare_datasets(inp,out,dataframe, ratio):
    '''conversion from pandas dataframe to ClassificationDataSet of numpy'''
    inp_dim = len(inp)
    out_dim = len(out)
    no_classes = 2
    alldata = ClassificationDataSet(inp_dim,out_dim,no_classes)
    inp = dataframe[inp]
    out = dataframe[out]
    #for [a,b,c],d in zip(inp.values,out.values):
    for i in range(len(inp.values)):
        d = out.values[i]
        if d=='up': d = 0
        elif d == 'down': d = 1
        else: d =2
        alldata.addSample(inp.values[i],d)
    tstdata_temp, trndata_temp = alldata.splitWithProportion( ratio )
    # to convert supervised datasets to classification datasets
    tstdata = trndata = ClassificationDataSet(inp_dim, out_dim, no_classes)
    for n in range(0, tstdata_temp.getLength()):
        tstdata.addSample( tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1] )
    for n in range(0, trndata_temp.getLength()):
        trndata.addSample( trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1])
    trndata._convertToOneOfMany()
    tstdata._convertToOneOfMany()
    return alldata, trndata, tstdata

# if __name__== '__main__':
#     hdfStore = loadHdf('store.h5')
#     df = load_data_frame('signals_nabil')
#     ds = df_to_cds(df)
#     trndata, tstdata = prepare_datasets(ds, 0.25)
