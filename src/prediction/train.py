
import logging
import sys
sys.path.insert(0, '../../src')
from prediction import prepareInput as pi
from preprocessing import moreIndicators as indi
from logger import log as log
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer
from pybrain.tools.validation import ModuleValidator, CrossValidator
from sklearn.metrics import accuracy_score, \
    precision_score, classification_report

# set up logger
log.setup_logging()
logger = logging.getLogger()
# load dataframe from csv file
df = pi.load_data_frame('sample_trend.csv')
# change datetime index to integer index
# TODO: manage issue with datetime index
df.index = range(len(df.index))
# change column name to match with indicator calculating module
df.columns = [
    'Transactions',
    'Traded_Shares',
    'Traded_Amount',
    'High',
    'Low',
    'Close',
    'signal']
# setup parameters
# TODO: use config file for parameter configuration
n = 20
prop = 0.20
# calculate and add indicators to dataframe
df = indi.EMA(df, n)
df = indi.RSI(df, n)
df = indi.MOM(df, n)

# prepate dataset for training and testing
input_features = ['RSI_' + str(n)]  # 'EMA_'+str(n),'Momentum_'+str(n)]
output_features = ['signal']
ds, trndata, tstdata = pi.prepare_datasets(
    input_features, output_features, df[20:], prop)


logger.info(
    'input features: ' +
    str(input_features) +
    str(n) +
    ', Output : ' +
    str(output_features))

# build network
hidden_dim = 20
logger.info('creating neural network')
fnn = buildNetwork(
    trndata.indim,
    hidden_dim,
    trndata.outdim,
    outclass=SoftmaxLayer)

logger.info('creating backprop Trainer')
# logger.info('neural network:\n'+str(fnn)+'\ninput_dim ='+str(trndata.indim)+', hidden_dim=' + str(hidden_dim) + ', output_dim ='+str(trndata.outdim))

# set up brckprop trainer
trainer = BackpropTrainer(
    fnn,
    dataset=trndata,
    momentum=0.01,
    verbose=True,
    weightdecay=0.01)

#modval = ModuleValidator()

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

# ## weights of connections
# print('weights of connections')
# ## input layer
# print(fnn['in'].outputbuffer[fnn['in'].offset])
# ## hidden layer
# print(fnn['hidden0'].outputbuffer[fnn['hidden0'].offset])
