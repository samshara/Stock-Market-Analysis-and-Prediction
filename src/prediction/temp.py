import sys
sys.path.insert(0,'../../src')
from prediction import prepareInput as pi
from preprocessing import indicators as indi

from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.tools.validation    import ModuleValidator, CrossValidator
from sklearn.metrics import accuracy_score,precision_score, classification_report

df = pi.load_data_frame('signal_trend.csv')
df.index = range(len(df.index))
# signal = df['signal']
# del df['signal']
df.columns = ['Transictions','Traded_Shares','Traded_Amount','High','Low','Close','signal']
n = 20
prop = 0.20
df = indi.RSI(df,n)
# df_norm = (df-df.mean())/(df.max()-df.min())
# df_norm['signal'] = signal

ds, trndata, tstdata = pi.prepare_datasets(['RSI_'+str(n),'signal'],df[20:],prop)


# build network
fnn = buildNetwork(trndata.indim, 20, trndata.outdim, outclass = SoftmaxLayer)

# set up brckprop trainer
trainer = BackpropTrainer(fnn, dataset = trndata, momentum = 0.01, verbose = True, weightdecay = 0.01 )

modval = ModuleValidator()

## start training iterations
# for i in range(100):
#     error = trainer.trainEpochs(1)
#     #cv = CrossValidator( trainer, trndata, n_folds=5, valfunc=modval.MSE )
#     #print("MSE %f @ %i" %( cv.validate(), i ))
#     trnresult = percentError(trainer.testOnClassData(),trndata['class'])
#     tstresult = percentError(trainer.testOnClassData(dataset = tstdata),tstdata['class'])
#     print("epoch: %4d"%trainer.totalepochs,"\ntrain error: %5.2f%%"%trnresult,"\ntest error: %5.2f%%"%tstresult)

trainer.trainUntilConvergence(verbose=True,
                              trainingData=trndata,
                              validationData=tstdata,
                              maxEpochs=15)
out = fnn.activateOnDataset(tstdata)
out = out.argmax(axis = 1)

target_names = ['up','down']
print(classification_report(tstdata['target'].argmax(axis=1),out,target_names=target_names))
print('accuracy= ',accuracy_score(tstdata['target'].argmax(axis=1),out))
# The precision is the ratio tp / (tp + fp)
print('precision= ',precision_score(tstdata['target'].argmax(axis=1),out))

# ## weights of connections
# print('weights of connections')
# ## input layer
# print(fnn['in'].outputbuffer[fnn['in'].offset])
# ## hidden layer
# print(fnn['hidden0'].outputbuffer[fnn['hidden0'].offset])
