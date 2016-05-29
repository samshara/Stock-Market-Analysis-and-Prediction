import prepareInput

from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

df = load_data_frame('signal.csv')
da = df_to_cds(df)
trndata, tstdata = prepare_datasets(ds,0.25)


# build network
fnn = buildNetwork(trndata.indim, 20, trndata.outdim, outclass = SoftmaxLayer, bias = True)

# set up brckprop trainer
trainer = BackpropTrainer(fnn, dataset = trndata, learningrate = 0.001, momentum = 0.1, verbose = True )

## start training iterations
for i in range(10):
    trainer.trainEpochs(1)
    trnresult = percentError(trainer.testOnClassData(),trndata['class'])
    tstresult = percentError(trainer.testOnClassData(dataset = tstdata),tstdata['class'])
    print("epoch: %4d"%trainer.totalepochs,"\ntrain error: %5.2f%%"%trnresult,"\ntest error: %5.2f%%"%tstresult)

# trainer.trainUntilConvergence(verbose=True,
#                               trainingData=trndata,
#                               validationData=tstdata,
#                               maxEpochs=10)
out = fnn.activateOnDataset(tstdata)

