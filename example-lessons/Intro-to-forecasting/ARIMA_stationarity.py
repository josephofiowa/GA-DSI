# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 10:09:38 2016

@author: JosephNelson
"""

# data https://datamarket.com/data/set/22w6/portland-oregon-average-monthly-bus-ridership-100-january-1973-through-june-1982-n114#!ds=22w6&display=line

%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
import seaborn as sns

import statsmodels.api as sm  
from statsmodels.tsa.stattools import acf  
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.seasonal import seasonal_decompose

bus = pd.read_csv('https://raw.githubusercontent.com/josephofiowa/GA-DSI/master/example-lessons/Intro-to-forecasting/portland-oregon-average-monthly-.csv', index_col=0)
bus.index.name=None
bus.reset_index(inplace=True)
bus.head()
bus.tail()

bus.drop(bus.index[115], inplace=True)
bus.drop(bus.index[114], inplace=True)


start = datetime.datetime.strptime("1973-01-01", "%Y-%m-%d")
date_list = [start + relativedelta(months=x) for x in range(0,114)] # edited to 115
bus['index'] =date_list
bus.set_index(['index'], inplace=True)
bus.index.name=None

len(date_list)  # check
len(bus.index)   # check

# riders
bus.columns= ['riders']
# df['riders'] = df.riders.apply(lambda x: int(x)*100)
bus['riders'] = bus.riders.apply(lambda x: int(x))
bus.riders

bus.riders.plot(figsize=(12,8), title= 'Monthly Ridership (100,000s)', fontsize=14)
# plt.savefig('month_ridership.png', bbox_inches='tight')   # optional save

decomposition = seasonal_decompose(bus.riders, freq=12)  
fig = plt.figure()  
fig = decomposition.plot()  
fig.set_size_inches(15, 8)
# plt.savefig('seasonal.png', bbox_inches='tight')   # optional save

# grab just one graphic doing the following:
seasonal = decomposition.seasonal 
seasonal.plot()

# define Dickey-Fuller test
from statsmodels.tsa.stattools import adfuller
def test_stationarity(timeseries):

    #Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)

    #Plot rolling statistics:
    fig = plt.figure(figsize=(12, 8))
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()
    
    #Perform Dickey-Fuller test:
    print 'Results of Dickey-Fuller Test:'
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print dfoutput 

# perform test
test_stationarity(bus.riders)

# first difference
bus['first_difference'] = bus.riders - bus.riders.shift(1)  
test_stationarity(bus.first_difference.dropna(inplace=False))

# seasonal difference
bus['seasonal_difference'] = bus.riders - bus.riders.shift(12)  
test_stationarity(bus.seasonal_difference.dropna(inplace=False))

# first seasonal difference
bus['seasonal_first_difference'] = bus.first_difference - bus.first_difference.shift(12)  
test_stationarity(bus.seasonal_first_difference.dropna(inplace=False))


# Source (but cleaned):
# https://github.com/seanabu/seanabu.github.io/blob/master/Seasonal_ARIMA_model_Portland_transit.ipynb

