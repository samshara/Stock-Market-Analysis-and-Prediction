# time series prediction of stock data
# using recurrent neural network with LSTM layer
from pybrain.datasets import SequentialDataSet
from itertools import cycle
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import LSTMLayer
from pybrain.supervised import RPropMinusTrainer
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '../../src')
from prediction import prepareInput as pi
from sklearn import preprocessing


df = pi.load_data_frame('sample_trend.csv')
df.columns = [
    'Transactions',
    'Traded_Shares',
    'Traded_Amount',
    'High',
    'Low',
    'Close',
    'signal']

data = df.Close.values[:500]
## TODO: write min_max normalization
# normalization
# cp = dataframe.pop(' Close Price')
# x = cp.values
min_max_scaler = preprocessing.MinMaxScaler()
data = min_max_scaler.fit_transform(data)
# dataframe[' Close Price'] = x_scaled

ds = SequentialDataSet(1, 1)
for sample, next_sample in zip(data, cycle(data[1:])):
    ds.addSample(sample, next_sample)
    
net = buildNetwork(1, 20, 1, 
                   hiddenclass=LSTMLayer, outputbias=False, recurrent=True)

trainer = RPropMinusTrainer(net, dataset=ds)
train_errors = [] # save errors for plotting later
EPOCHS_PER_CYCLE = 5
CYCLES = 10
EPOCHS = EPOCHS_PER_CYCLE * CYCLES
for i in range(CYCLES):
    trainer.trainEpochs(EPOCHS_PER_CYCLE)
    train_errors.append(trainer.testOnData())
    epoch = (i+1) * EPOCHS_PER_CYCLE
    print("\r epoch {}/{}".format(epoch, EPOCHS), end="")
    sys.stdout.flush()

print()
print("final error =", train_errors[-1])

predicted = []
for dat in data:
    predicted.append(net.activate(dat))
# data = min_max_scaler.inverse_transform(data)
# predicted = min_max_scaler.inverse_transform(predicted)
plt.plot(range(0,len(data)),data)
plt.plot(range(0,len(data)),predicted)
plt.show()

# plt.xlabel('epoch')
# plt.ylabel('error')
# plt.show()

# for sample, target in ds.getSequenceIterator(0):
#     print("               sample = %4.2f" % sample)
#     print("predicted next sample = %4.2f" % net.activate(sample))
#     print("   actual next sample = %4.2f" % target)
#     print()
