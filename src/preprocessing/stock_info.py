import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sys import argv

if len(argv) < 2:
    exit('Usage: %s stockname(Uppercase)' % argv[0])
dataSource = '../Data_Cleaner/Stock_Data_Cleaned/'
stocks=[]
for i in range(1,len(argv)):
    stocks.append(argv[i].upper())
# print(stocks)    
# stock = argv[1].upper()
for stock in stocks:
    source = dataSource+stock+'.csv'
    try:
        dataframe = pd.read_csv(source, index_col = 0, parse_dates = True)
    except Exception as e:
        print("Unexpected error:"+str(e))
    if dataframe.empty:
        print("empty"+source)
    #print(dataframe.head())
    #print(dataframe.describe())
    ## To plot
    plt.figure()
    #plt.plot(dataframe[' Close Price'])
    #dataframe[' Close Price'].plot(title ='nabil',label = stock) #title = stock)
    #calculating moving avarage
    if(len(stocks)== 1):
        data_mean10 = pd.rolling_mean(dataframe[' Close Price'],window=10)
        data_mean50 = pd.rolling_mean(dataframe[' Close Price'],window=50)
        df10 = pd.DataFrame(data_mean10)
        df50 = pd.DataFrame(data_mean50)
        plt.plot(df10, label = 'window=10')
        plt.plot(df50, label = 'window=50')
    ## Display the plot
plt.legend(loc=2,borderaxespad=0.)
plt.show()
