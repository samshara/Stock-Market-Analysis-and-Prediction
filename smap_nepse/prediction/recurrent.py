# time series prediction of stock data
# using recurrent neural network with LSTM layer
from pybrain.datasets import SequentialDataSet
from itertools import cycle
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import LSTMLayer
from pybrain.supervised import RPropMinusTrainer
from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.customxml.networkreader import NetworkReader
import matplotlib.pyplot as plt
import os.path
import sys
#sys.path.insert(0, '../../smap_nepse')
from smap_nepse.prediction import prepareInput as pi
from sklearn import preprocessing
import numpy as np

__author__ = "Semanta Bhandari"
__copyright__ = ""
__credits__ = ["Sameer Rai","Sumit Shrestha","Sankalpa Timilsina"]
__license__ = ""
__version__ = "0.1"
__email__ = "semantabhandari@gmail.com"

def rnn():
    # load dataframe from csv file
    df = pi.load_data_frame('../../data/NABIL.csv')
    # column name to match with indicator calculating modules
    # TODO: resolve issue with column name
    df.columns = [
        'Transactions',
        'Traded_Shares',
        'Traded_Amount',
        'High',
        'Low',
        'Close']
     
    data = df.Close.values
    # TODO: write min_max normalization
    # normalization
    # cp = dataframe.pop(' Close Price')
    # x = cp.values
    temp = np.array(data).reshape(len(data),1)
    min_max_scaler = preprocessing.MinMaxScaler()
    data = min_max_scaler.fit_transform(temp)
    # dataframe[' Close Price'] = x_scaled
     
    # prepate sequential dataset for pyBrain rnn network
    ds = SequentialDataSet(1, 1)
    for sample, next_sample in zip(data, cycle(data[1:])):
        ds.addSample(sample, next_sample)
     
    # build rnn network with LSTM layer
    # if saved network is available
    if(os.path.isfile('random.xml')):
        net = NetworkReader.readFrom('network.xml')
    else:
        net = buildNetwork(1, 20, 1, 
                           hiddenclass=LSTMLayer, outputbias=False, recurrent=True)
     
    # build trainer
    trainer = RPropMinusTrainer(net, dataset=ds, verbose = True)
    train_errors = [] # save errors for plotting later
    EPOCHS_PER_CYCLE = 5
    CYCLES = 5
    EPOCHS = EPOCHS_PER_CYCLE * CYCLES
    for i in range(CYCLES):
        trainer.trainEpochs(EPOCHS_PER_CYCLE)
        train_errors.append(trainer.testOnData())
        epoch = (i+1) * EPOCHS_PER_CYCLE
        print("\r epoch {}/{}".format(epoch, EPOCHS), end="")
        sys.stdout.flush()
    # save the network
    NetworkWriter.writeToFile(net,'network.xml')
        
    print()
    print("final error =", train_errors[-1])
     
    predicted = []
    for dat in data:
        predicted.append(net.activate(dat)[0])
    # data = min_max_scaler.inverse_transform(data)
    # predicted = min_max_scaler.inverse_transform(predicted)
    predicted_array = min_max_scaler.inverse_transform(np.array(predicted).reshape(-1,1))
    print(predicted_array[-1])
    plt.figure()
     
    legend_actual, = plt.plot(range(0, len(data)),temp, label = 'actual', linestyle = '--', linewidth = 2, c = 'blue')
    legend_predicted, = plt.plot(range(0, len(data)), predicted_array, label = 'predicted', linewidth = 1.5, c='red')
    plt.legend(handles=[legend_actual, legend_predicted])
    plt.savefig('error.png')
    plt.show()
     
    # plt.plot(range(0,len(train_errors)),train_errors)
    # plt.xlabel('epoch')
    # plt.ylabel('error')
    # plt.show()
     
    # for sample, target in ds.getSequenceIterator(0):
    #     print("               sample = %4.2f" % sample)
    #     print("predicted next sample = %4.2f" % net.activate(sample))
    #     print("   actual next sample = %4.2f" % target)
    #     print()
rnn()
