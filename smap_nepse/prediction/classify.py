import numpy as np
import pandas as pd
import logging
import sys
sys.path.insert(0, '../../smap-nepse')
from prediction import prepareInput as pi
from preprocessing import moreIndicators as indi
from logger import log as log
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
import pickle
from datetime import datetime

__author__ = "Semanta Bhandari"
__copyright__ = ""
__credits__ = ["Sameer Rai","Sumit Shrestha","Sankalpa Timilsina"]
__license__ = ""
__version__ = "0.1"
__email__ = "semantabhandari@gmail.com"

# set up logger
log.setup_logging()
logger = logging.getLogger()
logger.info('+++++++++++++++++++++++++')
logger.info('file: classify.py')
logger.info('setup check')


def load_dataset(stockname, window = 1):
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
    dataframe = pi.signal_updown(dataframe, window)
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

def prepareDataForClassification(dataframe, start_test):
    """
    generates categorical output column, attach to dataframe 
    label the categories and split into train and test
    Parameters:
    dataframe: pandas dataframe
    start_test: size of training dataset
    Returns:
    X_train: feature dataset for training
    y_train: target dataset for training[0: down, 1: up]
    X_test: feature dataset for testing
    y_test: target dataset for testing[0: down, 1: up]
    """
    print('preparing dataset...')
    le = preprocessing.LabelEncoder()
    n = 20
    dataframe = indi.EMA(dataframe, n)
    dataframe = indi.RSI(dataframe, n)
    dataframe = indi.MOM(dataframe, n)
    features = ['RSI_'+str(n)]#, 'EMA_'+str(n)]
    dataframe.signal = le.fit(dataframe.signal).transform(dataframe.signal)
    
    # X = dataframe[features][20:]    
    # y = dataframe.signal[20:]
    X = dataframe[features].values
    y = dataframe.signal.values
    
    X_train = X[:start_test]
    y_train = y[:start_test]
    
    X_test = X[start_test:]
    y_test = y[start_test:]
    
    return X_train, y_train, X_test, y_test   

def performClassification(X_train, y_train, X_test, y_test, method, parameters, fout, savemodel):
    """
    performs classification on daily returns using several algorithms (method).
    Parameters:
    method : algorithm for classificaiton
    parameters : of parameters passed to the classifier (if any)
    fout : with name of stock to be predicted
    savemodel : If TRUE saves the model to pickle file
    """
   
    if method == 'RF':   
        return performRFClass(X_train, y_train, X_test, y_test, parameters, fout, savemodel)
    elif method == 'DT':
        return performDTClass(X_train, y_train, X_test, y_test, parameters, fout, savemodel)
    elif method == 'KNN':
        return performKNNClass(X_train, y_train, X_test, y_test, parameters, fout, savemodel)
    elif method == 'SVM':   
        return performSVMClass(X_train, y_train, X_test, y_test, parameters, fout, savemodel)
    elif method == 'ADA':
        return performAdaBoostClass(X_train, y_train, X_test, y_test, parameters, fout, savemodel)

def performRFClass(X_train, y_train, X_test, y_test, parameters, fout, savemodel):
    """
    Random Forest Binary Classification
    """
    clf = RandomForestClassifier(n_estimators=1000, n_jobs=-1)
    clf.fit(X_train, y_train)
    
    if savemodel == True:
        #fname_out = '{}-{}.pickle'.format(fout, datetime.now())
        fname_out = fout + '.pickle'
        with open(fname_out, 'wb') as f:
            pickle.dump(clf, f, -1)    
    
    accuracy = clf.score(X_test, y_test)
    
    return accuracy

def performKNNClass(X_train, y_train, X_test, y_test, parameters, fout, savemodel):
    """
    KNN binary Classification
    """
    clf = KNeighborsClassifier(3)
    clf.fit(X_train, y_train)

    if savemodel == True:
        #fname_out = '{}-{}.pickle'.format(fout, datetime.now().date())
        fname_out = fout+'.pickle'
        with open(fname_out, 'wb') as f:
            pickle.dump(clf, f, -1)    
    
    accuracy = clf.score(X_test, y_test)
    
    return accuracy

def performSVMClass(X_train, y_train, X_test, y_test, parameters, fout, savemodel):
    """
    SVM binary Classification
    """
    # c = parameters[0]
    # g =  parameters[1]
    clf = SVC(kernel = 'linear', C = 0.025)
    clf.fit(X_train, y_train)

    if savemodel == True:
        #fname_out = '{}-{}.pickle'.format(fout, datetime.now().date())
        fname_out = fout+'.pickle'
        with open(fname_out, 'wb') as f:
            pickle.dump(clf, f, -1)    
    
    accuracy = clf.score(X_test, y_test)
    
    return accuracy

def performAdaBoostClass(X_train, y_train, X_test, y_test, parameters, fout, savemodel):
    """
    Ada Boosting binary Classification
    """
    # n = parameters[0]
    # l =  parameters[1]
    clf = AdaBoostClassifier()
    clf.fit(X_train, y_train)

    if savemodel == True:
        #fname_out = '{}-{}.pickle'.format(fout, datetime.now())
        fname_out = fout + '.pickle'
        with open(fname_out, 'wb') as f:
            pickle.dump(clf, f, -1)    
    
    accuracy = clf.score(X_test, y_test)
    
    return accuracy

def performDTClass(X_train, y_train, X_test, y_test, parameters, fout, savemodel):
    """
    Decision Tree Classification 
    """
    # n = parameters[0]
    # l =  parameters[1]
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    if savemodel == True:
        #fname_out = '{}-{}.pickle'.format(fout, datetime.now())
        fname_out = fout+'.pickle'
        with open(fname_out, 'wb') as f:
            pickle.dump(clf, f, -1)    
    
    accuracy = clf.score(X_test, y_test)
    
    return accuracy

#TODO: use hdf datastructure for dataframes
stockname = 'NABIL'
names = ['DT', 'KNN', 'SVM']
dataframe = load_dataset('../../data/cleaneddata/'+stockname+'.csv')
X_train,y_train,X_test,y_test = prepareDataForClassification(dataframe,1500)
#acc = performClassification(X_train[20:], y_train[20:], X_test, y_test, 'SVM', None, '../../networks/'+stockname+':svm', 1)
for name in names:
    acc = performClassification(X_train[20:], y_train[20:], X_test, y_test, name, None, '../../networks/' + stockname + ':' + name, 1)
    print(name, ':', acc)

# output::
# loading dataset...
# preparing dataset...
# RF : 0.727549467275
# DT : 0.727549467275
# KNN : 0.770167427702
# SVM : 0.814307458143
# ADA : 0.820395738204
