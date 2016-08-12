import numpy as np
import pandas as pd

from sklearn.linear_model import Lasso

from sklearn.preprocessing import StandardScaler


	

df = pd.read_csv("NABIL.csv")
df.drop(df.columns[[0,1,9,13,14]], axis=1, inplace=True)
#print(df.columns)
df.drop(df.index[:19],inplace=True)
scaler = StandardScaler()

#df['Price']=df['Closing Price'].shift(-1)
#df=df[:-1]
#Y = df['Price']

#df1 = df.drop('Price', axis=1)
X = scaler.fit_transform(df)
Y=df['Closing Price']


names = df.columns

lasso = Lasso(alpha=.3)
lasso.fit(X, Y)
lst = sorted(zip(lasso.coef_, names), key=lambda x: x[0], reverse=True)
print(lst)