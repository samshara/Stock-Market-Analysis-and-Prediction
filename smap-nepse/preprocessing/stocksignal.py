import pandas as pd
import numpy as np 

df=pd.read_csv('NABIL.csv')
#ratio=int(len(df.index)*0.7)

#Generate buy/sell/hold signal using RSI 
def signal(df):
	Signal=[]
	for i in range(len(df.index)):
		if (i<16):
			Signal.append('Nan')
		else:
			if (df.iloc[i]['Closing Price'] > df.iloc[i-1]['Closing Price']) and (float(df.iloc[i]['Relative Strength Index'])>float(df.iloc[i-1]['Relative Strength Index'])) and (float(df.iloc[i]['Relative Strength Index'])>50):
				Signal.append('Buy')
			elif (df.iloc[i]['Closing Price'] < df.iloc[i-1]['Closing Price']) and (float(df.iloc[i]['Relative Strength Index'])<float(df.iloc[i-1]['Relative Strength Index'])) and (float(df.iloc[i]['Relative Strength Index'])<50):
				Signal.append('Sell')
			else:
				Signal.append('Hold')
	return Signal

Signal=signal(df)
df['Signal']=Signal
df.to_csv('NABIL.csv')








	#TODO: RSI fill class values
	#select features based on RSI