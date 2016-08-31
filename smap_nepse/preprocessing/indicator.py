import pandas as pd

def RSI(data,window_length=14):

    # Get only closing price
    close = data['Closing Price']
    # Get difference in price
    delta = close.diff()

    # Make positive gains and negative gains Series
    up, down = delta.copy(), delta.copy()
    down[down > 0] = 0
    up[up < 0] = 0

    # Calculate the EWMA
    roll_up1 = up.ewm(span=window_length).mean()
    roll_down1 = down.abs().ewm(span=window_length).mean()

    # Calculate RSI based on EWMA
    RS1 = roll_up1 / roll_down1
    RSI1 = pd.Series(100.0 - (100.0 / (1.0 + RS1)), name='RSI_FWMA')

    # Calculate the SMA
    roll_up2 = up.rolling(window_length).mean()
    roll_down2 = down.abs().rolling(window_length).mean()

    # Calculate RSI based on SMA
    RS2 = roll_up2 / roll_down2
    RSI2 = pd.Series(100.0 - (100.0 / (1.0 + RS2)), name='RSI_SMA')
    data = pd.concat([data, RSI1, RSI2], axis=1)
    return data

def movingaverage(data,window_length=14):
    # Get only closing price
    close = data['Closing Price']

    ewma = close.ewm(span=window_length).mean().rename('CP_EMA')
    sma =  close.ewm(span=window_length).mean().rename('CP_SMA')

    data = pd.concat([data, ewma, sma], axis=1)
    return data

def macd(data):
    close = data['Closing Price']

    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    ema9 = close.ewm(span=9).mean()
    macd = (ema12 - ema26).rename('MACD')
    macd_signal = macd.ewm(span=9).mean().rename('MACD_SIGNAL')
    macd_hist = (macd - macd_signal).rename('MACD_HIST')

    data = pd.concat([data,macd,macd_signal,macd_hist],axis=1)
    return data
