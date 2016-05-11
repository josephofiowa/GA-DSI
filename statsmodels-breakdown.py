# -*- coding: utf-8 -*-
"""
Created on Mon May 9 08:02:51 2016

@author: JosephNelson
"""


'''
http://statsmodels.sourceforge.net/devel/examples/notebooks/generated/ols.html
'''

from __future__ import print_function
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std

np.random.seed(9876789)

nsample = 100
x = np.linspace(0, 10, 100)
x.shape

X = np.column_stack((x, x**2))
X.shape

beta = np.array([1, 0.1, 10])
beta

e = np.random.normal(size=nsample)
e.shape

X = sm.add_constant(X)
y = np.dot(X, beta) + e

model = sm.OLS(y, X)
results = model.fit()
print(results.summary())

print('Parameters: ', results.params)
print('R2: ', results.rsquared)
