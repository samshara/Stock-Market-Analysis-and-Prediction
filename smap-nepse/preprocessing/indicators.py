import pandas as pd
import numpy as np
import os
import glob


#function to calculate typical price
def TypicalPrice(df):     
    TP=[]                   #typical price
    for i in range(len(df.index)):
        TP.append((df.iloc[i]['Closing Price'] + df.iloc[i]['Maximum Price'] + df.iloc[i]['Minimum Price'])/3)
        
    return TP

#function to calculate chaikin money flow indicator
#Ranges from -1 to 1
#Some correction to be made

def Chaikin(df):    
    CLV=[]              #Closing Location Value which shows accumulation/distribution
    CMF=[]              #Chaikin Money Flow Indicator

    for i in range(len(df.index)):
        #CLV=[(close-low)-(high-close)]/(high-low)

        CLV.append(((df.iloc[i]['Closing Price']-df.iloc[i]['Minimum Price'])-(df.iloc[i]['Maximum Price']- df.iloc[i]['Closing Price']))/ (df.iloc[i]['Maximum Price'] -df.iloc[i]['Minimum Price']))
    
    #CMF=Sum(CLV*volume)/Sum(Volume) for last 20 days    
    for i in range(len(df.index)):
        if i<19:
            CMF.append('Nan')
        else:
            numer=0
            denom=0
            for j in range(i-19,i+1):
                numer=numer+(CLV[j]*df.iloc[j]['Traded Shares'])
                denom=denom+(df.iloc[j]['Traded Shares'])
            CMF.append(numer/denom)
    return CMF
#if CMF > 0.25 ==> bullish signal
#if CMF < -0.25 ==> a bearish signal
#if CMF < 0 while the price is rising, it indicates a probable reversal


#function to calculate RSI
#RSI=100-100/(1+RS)
#Ranges from 0 to 100
#Measures the relative strength of up and down movement in prices
#RSI>80 overbought, RSI<20 oversold, RSI between 20 and 80 neutral
def RSI(df):
    N=14             #Number of RSI periods
    RSI=[]
    for i in range(len(df.index)):
        if i<N:
            RSI.append('Nan')
        else:
            up=[]
            down=[]
            for j in range(i-N,i):
                diff=df.iloc[j+1]['Closing Price']-df.iloc[j]['Closing Price']
                if diff>0:
                    up.append(diff)
                    down.append(0)
                elif diff<0:
                    up.append(0)
                    down.append(-diff)
                else:
                    up.append(0)
                    down.append(0)


            upavg=sum(up)/float(N)      #Average of all up moves in N periods
            downavg=sum(down)/float(N)  #Average of all down moves in N periods
            if downavg==0:
                RSI.append(100)
            else:
                RS=upavg/downavg        #Relative Strength
                RSI.append(100-100/(1+RS))


    return RSI

#20 day simple moving average
def SimpleMovingAverage(df):
    N=20
    SMA=[]
    for i in range(len(df.index)):
        if i<N-1:
            SMA.append('Nan')
        else:
            sum=0
            for j in range(i+1-N,i+1):
                sum=sum+df.iloc[j]['Closing Price']
            SMA.append(sum/N)
    return SMA


#@0 day exponential moving average
def ExpMovingAverage(df):
    N=20
    EMA=[]
    k=2/(N+1)
    EMA.append(df.iloc[0]['Closing Price'])

    for i in range(1,len(df.index)):
        EMA.append((df.iloc[i]['Closing Price']*k) + (EMA[i-1]*(1-k)))
    return EMA


def Indicators(path):
    for file in glob.glob(path):
        df=pd.read_csv(file)

        TP=TypicalPrice(df)
        df['Typical Price']=TP


        CMF=Chaikin(df)
        df['Chaikin Money Flow']=CMF

        RS=RSI(df)
        df['Relative Strength Index']=RS

        SMA=SimpleMovingAverage(df)
        df['Simple Moving Average']=SMA

        EMA=ExpMovingAverage(df)
        df['Exponential Moving Average']=EMA

        df.to_csv(file,index=False)




Indicators('../cleaneddata/*.csv')











    

