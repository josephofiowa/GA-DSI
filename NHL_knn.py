# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:55:26 2016

@author: JosephNelson
"""


import pandas as pd
NHL = pd.read_csv('NHL_data.csv')
NHL.head()
NHL.describe()
NHL.shape

NHL.isnull().sum()

'''
K-Nearest Neighbors Classification
'''

# store feature matrix in "X"
feature_cols = ['CF%', 'GF', 'Sh%', 'PDO']
X = NHL[feature_cols]

# store response vector in "y"
y = NHL.PTS

# check X's type
print type(X)
print type(X.values)

# check y's type
print type(y)
print type(y.values)


# check X's shape (n = number of observations, p = number of features)
print X.shape

# check y's shape (single dimension with length n)
print y.shape

from sklearn.neighbors import KNeighborsClassifier
# make an instance of a KNeighborsClassifier object
knn = KNeighborsClassifier(n_neighbors=1)
type(knn)

print knn

knn.fit(X, y)

# predict the response values for the observations in X ("test the model")
knn.predict(X)

# store the predicted response values
y_pred_class = knn.predict(X)

# compute classification accuracy
from sklearn import metrics
print metrics.accuracy_score(y, y_pred_class)

'''
Train, test, split
'''

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)

# STEP 1: split X and y into training and testing sets (using random_state for reproducibility)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=99)

# STEP 2: train the model on the training set (using K=1)
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)

# STEP 3: test the model on the testing set, and check the accuracy
y_pred_class = knn.predict(X_test)
print metrics.accuracy_score(y_test, y_pred_class)

# test with 50 neighbors
knn = KNeighborsClassifier(n_neighbors=50)
knn.fit(X_train, y_train)
y_pred_class = knn.predict(X_test)
print metrics.accuracy_score(y_test, y_pred_class)

# test with 65 neighbors
knn = KNeighborsClassifier(n_neighbors=64)
knn.fit(X_train, y_train)
y_pred_class = knn.predict(X_test)
print metrics.accuracy_score(y_test, y_pred_class)

# examine the class distribution
y_test.value_counts()

# compute null accuracy
y_test.value_counts().head(1) / len(y_test)


# calculate TRAINING ERROR and TESTING ERROR for K=1 through 64

k_range = range(1, 64)
training_error = []
testing_error = []

for k in k_range:

    # instantiate the model with the current K value
    knn = KNeighborsClassifier(n_neighbors=k)

    # calculate training error
    knn.fit(X, y)
    y_pred_class = knn.predict(X)
    training_accuracy = metrics.accuracy_score(y, y_pred_class)
    training_error.append(1 - training_accuracy)
    
    # calculate testing error
    knn.fit(X_train, y_train)
    y_pred_class = knn.predict(X_test)
    testing_accuracy = metrics.accuracy_score(y_test, y_pred_class)
    testing_error.append(1 - testing_accuracy)
    
    
# allow plots to appear in the notebook
%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# create a DataFrame of K, training error, and testing error
column_dict = {'K': k_range, 'training error':training_error, 'testing error':testing_error}
df = pd.DataFrame(column_dict).set_index('K').sort_index(ascending=False)
df.head()

# plot the relationship between K (HIGH TO LOW) and TESTING ERROR
df.plot(y='testing error')
plt.xlabel('Value of K for KNN')
plt.ylabel('Error (lower is better)')
plt.savefig('KNN.png')

