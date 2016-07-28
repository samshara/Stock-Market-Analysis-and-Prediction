import logging
import os.path
import sys
sys.path.insert(0, '../../src')
from prediction import prepareInput as pi
from preprocessing import moreIndicators as indi
from logger import log as log
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer
from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.customxml.networkreader import NetworkReader
from pybrain.tools.validation import ModuleValidator, CrossValidator
from sklearn.metrics import accuracy_score, \
    precision_score, classification_report

__author__ = "Semanta Bhandari"
__copyright__ = ""
__credits__ = ["Sameer Rai","Sumit Shrestha","Sankalpa Timilsina"]
__license__ = ""
__version__ = "0.1"
__email__ = "semantabhandari@gmail.com"

    
def load_dataset(stockname):
    '''
    load dataset from csv filename

    Parameters:
    stockname: name of the csv file of stock data

    Returns:
    dataframe: pandas dataframe
    '''
    print('loading dataset...')
    # load dataframe from csv file
    dataframe = pi.load_data_frame(stockname)
    # change datetime index to integer index
    # TODO: manage issue with datetime index
    dataframe.index = range(len(dataframe.index))
    # change column name to match with indicator calculating module
    dataframe.columns = [
        'Transactions',
        'Traded_Shares',
        'Traded_Amount',
        'High',
        'Low',
        'Close',
        'signal']
    return dataframe

def select_features(dataframe):
    '''
    select input and output features to prepate training and testing dataset
    
    Parameters:
    dataframe: dataframe of the stock data

    Returns:
    trndata: training dataset
    tstdata: testing dataset
    '''
    #TODO: dynamic feature selection
    print('selecting features...')
    # calculate and add indicators to dataframe
    dataframe = indi.EMA(dataframe, n)
    dataframe = indi.RSI(dataframe, n)
    dataframe = indi.MOM(dataframe, n)

    # prepate dataset for training and testing
    input_features = ['RSI_' + str(n)]#,'EMA_'+str(n)]#'Momentum_'+str(n)]
    output_features = ['signal']
    ds, trndata, tstdata = pi.prepare_datasets(
        input_features, output_features, dataframe[20:], prop)

    print('input features: ' + str(input_features)  +', Output : ' + str(output_features))
    logger.info(
        'input features: ' +
        str(input_features) +
        ', Output : ' +
        str(output_features))
    return trndata, tstdata

def build_network(trndata, tstdata, hidden_dim, fout, load_network):
    '''
    build ANN network with backpropagation trainer

    Parameters:
    trndata: training dataset
    tstdata: testing dataset
    hidden_dim: no of neuron in hidden layer
    fout: filename to load saved network
    load_network: True: load network, False: dont load network

    Returns:
    fnn: feedforward neural network
    trainer: back propagation trainer
    '''
    # build network
    print('creating neural network...')
    logger.info('creating neural network')
    if(os.path.isfile('ann.xml')):
        fnn = NetworkReader.readFrom('ann.xml')
    else:
        fnn = buildNetwork(
            trndata.indim,
            hidden_dim,
            trndata.outdim,
            outclass=SoftmaxLayer)

    print('creating backprop Trainer...')
    logger.info('creating backprop Trainer')
    # logger.info('neural network:\n'+str(fnn)+'\ninput_dim ='+str(trndata.indim)+', hidden_dim=' + str(hidden_dim) + ', output_dim ='+str(trndata.outdim))
     
    # set up brckprop trainer
    trainer = BackpropTrainer(
        fnn,
        dataset=trndata,
        momentum=0.01,
        verbose=True,
        weightdecay=0.01)
    return fnn, trainer


def train_network(trndata,tstdata,fnn,trainer):
    ''' 
    train the network using trainer

    Parameters:
    trndata: training dataset
    tstdata: testing dataset
    fnn: feed forward NN
    trainer: backprop trainer
    '''
    print('training and testing network')
    logger.info('training and testing network')
    # start training iterations
    # for i in range(100):
    #     error = trainer.trainEpochs(1)
    #     #cv = CrossValidator( trainer, trndata, n_folds=5, valfunc=modval.MSE )
    #     #print("MSE %f @ %i" %( cv.validate(), i ))
    #     trnresult = percentError(trainer.testOnClassData(),trndata['class'])
    #     tstresult = percentError(trainer.testOnClassData(dataset = tstdata),tstdata['class'])
    #     print("epoch: %4d"%trainer.totalepochs,"\ntrain error: %5.2f%%"%trnresult,"\ntest error: %5.2f%%"%tstresult)
     
    # train the network until convergence
    trainer.trainUntilConvergence(verbose=True,
                                  trainingData=trndata,
                                  validationData=tstdata,
                                  maxEpochs=5)
    NetworkWriter.writeToFile(fnn,'ann.xml')
    
def activate_network(tstdata, fnn):
    print('activating network on data')
    # activate network for test data
    out = fnn.activateOnDataset(tstdata)
    # index of  maximum value gives the class
    out = out.argmax(axis=1)

    # result analysis, uses scikitlearn metrics
    target_names = ['up', 'down']
    print(
        classification_report(
            tstdata['target'].argmax(
                axis=1),
            out,
            target_names=target_names))
    print('accuracy= ', accuracy_score(tstdata['target'].argmax(axis=1), out))
    # The precision is the ratio tp / (tp + fp)
    print('precision= ', precision_score(tstdata['target'].argmax(axis=1), out))
    logger.info(
        '\n' +
        classification_report(
            tstdata['target'].argmax(
                axis=1),
            out,
            target_names=target_names))

if __name__== '__main__':
    # setup parameters
    # TODO: use config file for parameter configuration
    n = 20
    prop = 0.20

    # set up logger
    log.setup_logging()
    logger = logging.getLogger()
    logger.info('+++++++++++++++++++++++++')
    logger.info('file: train.py')

    logger.info('init logging..')
    dataframe = load_dataset('sample_trend.csv')
    trndata, tstdata = select_features(dataframe)
    fnn, trainer = build_network(trndata, tstdata, 20, 'ann.xml',1)
    train_network(trndata, tstdata, fnn, trainer)
    activate_network(tstdata, fnn)

# ## weights of connections
# print('weights of connections')
# ## input layer
# print(fnn['in'].outputbuffer[fnn['in'].offset])
# ## hidden layer
# print(fnn['hidden0'].outputbuffer[fnn['hidden0'].offset])
