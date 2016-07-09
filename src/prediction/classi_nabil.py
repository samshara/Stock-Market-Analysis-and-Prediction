# will be removed later
from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules import SoftmaxLayer

from sklearn import preprocessing
import pandas as pd

# read dataframe from csv file
dataframe = pd.read_csv(
    '../../data/signals_nabil.csv',
    index_col=0,
    parse_dates=True)
# normalization
# cp = dataframe.pop(' Close Price')
# x = cp.values
# min_max_scaler = preprocessing.MinMaxScaler()
# x_scaled = min_max_scaler.fit_transform(x)
# dataframe[' Close Price'] = x_scaled

# prepare calssicication dataset
alldata = ClassificationDataSet(
    1, 1, nb_classes=3, class_labels=[
        'hold', 'sell', 'buy'])
inp = dataframe[['madiff', 'signal']]
for b, c in inp.values:
    # if c=='hold': c = 0
    # elif c == 'buy': c = 1
    # else: c =2
    alldata.addSample([b], c)
tstdata_temp, trndata_temp = alldata.splitWithProportion(0.25)

# to convert supervised datasets to classification datasets
tstdata = ClassificationDataSet(1, 1, nb_classes=3)
for n in range(0, tstdata_temp.getLength()):
    tstdata.addSample(
        tstdata_temp.getSample(n)[0],
        tstdata_temp.getSample(n)[1])
trndata = ClassificationDataSet(1, 1, nb_classes=3)
for n in range(0, trndata_temp.getLength()):
    trndata.addSample(
        trndata_temp.getSample(n)[0],
        trndata_temp.getSample(n)[1])
#
trndata._convertToOneOfMany()
tstdata._convertToOneOfMany()
#
# print ("Number of training patterns: ", len(trndata))
# print ("Input and output dimensions: ", trndata.indim, trndata.outdim)
# print ("(input, target, class):")
# print (trndata['input'][0], trndata['target'][0], trndata['class'][0])

# build network
fnn = buildNetwork(
    trndata.indim,
    20,
    trndata.outdim,
    outclass=SoftmaxLayer,
    bias=True)
# set up brckprop trainer
trainer = BackpropTrainer(
    fnn,
    dataset=trndata,
    learningrate=0.001,
    momentum=0.1,
    verbose=True)

# start training iterations
# for i in range(10):
#     trainer.trainEpochs(1)
#     trnresult = percentError(trainer.testOnClassData(),trndata['class'])
#     tstresult = percentError(trainer.testOnClassData(dataset = tstdata),tstdata['class'])
#     print("epoch: %4d"%trainer.totalepochs,"\ntrain error: %5.2f%%"%trnresult,"\ntest error: %5.2f%%"%tstresult)

trainer.trainUntilConvergence(verbose=True,
                              trainingData=trndata,
                              validationData=tstdata,
                              maxEpochs=10)
out = fnn.activateOnDataset(tstdata)
