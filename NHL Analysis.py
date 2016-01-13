# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 23:32:33 2015

@author: JosephNelson
"""

import pandas as pd
NHL = pd.read_csv('NHL_data.csv')
NHL.head()
NHL.describe()
NHL.shape

NHL.isnull().sum()


import matplotlib.pyplot as plt

# display plots in the notebook
%matplotlib inline

# list available plot styles
plt.style.available

# change to a different style
plt.style.use('ggplot')

# increase default figure and font sizes for easier viewing
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 14

# sort the GF by teams and split
NHL.GF.order().values
# compare with histogram
NHL.GF.plot(kind='hist', bins=10)

# add title and labels
NHL.GF.plot(kind='hist', bins=10, title='Goals by Season 09-12')
plt.xlabel('Goals')
plt.ylabel('Frequency')

# repeat for PIM
# sort the PIM by teams and split
NHL.PIM.order().values
# compare with histogram
NHL.PIM.plot(kind='hist', bins=12, title='PIM by Season 09-12')
plt.xlabel('Penalty Minutes')
plt.ylabel('Frequency')

# compare with density plot (smooth version of a histogram)
NHL.GF.plot(kind='density', xlim=(0, 200))


'''
Scatter Plots
'''

# select the GF and PIM columns and sort by GF because why not
NHL[['GF', 'PIM']].sort('GF').values

# compare with scatter plot
NHL.plot(kind='scatter', x='PIM', y='GF') # greeeaat relationship
plt.savefig('scat_PIM_GF.png')


# GF and shooting percentage
NHL[['GF', 'Sh%']].sort('GF').values
NHL.plot(kind='scatter', x='Sh%', y='GF')
plt.savefig('scat_Sh%_GF.png')


# GF and PDO
NHL[['GF', 'PDO']].sort('GF').values
NHL.plot(kind='scatter', x='PDO', y='GF')
plt.savefig('scat_GF_PDO.png')


# GF and CF%
NHL[['GF', 'CF%']].sort('GF').values
NHL.plot(kind='scatter', x='GF', y='CF%')

# PTS and PIM
NHL[['PTS', 'PIM']].sort('PTS').values
NHL.plot(kind='scatter', x='PIM', y='PTS')


# PTS and GF
NHL[['PTS', 'GF']].sort('GF').values
NHL.plot(kind='scatter', x='GF', y='PTS')
# add transparency
NHL.plot(kind='scatter', x='GF', y='PTS', alpha=0.3) # looks bad

# PTS and PDO
NHL[['PTS', 'PDO']].sort('PDO').values
NHL.plot(kind='scatter', x='PDO', y='PTS')

# PTS and Sv%
NHL[['PTS', 'Sv%']].sort('Sv%').values
NHL.plot(kind='scatter', x='Sv%', y='PTS')

# PTS and GA60
NHL[['PTS', 'GA60']].sort('GA60').values
NHL.plot(kind='scatter', x='GA60', y='PTS')

# PTS and CF%
NHL[['PTS', 'CF%']].sort('CF%').values
NHL.plot(kind='scatter', x='CF%', y='PTS')
plt.savefig('scat_PTS_CF%.png')



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


'''
Linear Regression
'''

import seaborn as sns

# Seaborn scatter plot with regression line
sns.lmplot(x='GF', y='PTS', data=NHL, aspect=1.5, scatter_kws={'alpha':0.2})


# create X and y

feature_cols = ['CF%', 'GF', 'Sh%', 'PDO']
X = NHL[feature_cols]
y = NHL.PTS

# import, instantiate, fit
from sklearn.linear_model import LinearRegression
linreg = LinearRegression()
linreg.fit(X, y)

# print the coefficients
print linreg.intercept_
print linreg.coef_

# explore more features
feature_cols = ['CF%', 'GF', 'Sh%', 'PDO']

# multiple scatter plots in Seaborn
sns.pairplot(NHL, x_vars=feature_cols, y_vars='PTS', kind='reg')
plt.savefig('pair_plots.png') 


# multiple scatter plots in Pandas
fig, axs = plt.subplots(1, len(feature_cols), sharey=True)
for index, feature in enumerate(feature_cols):
    NHL.plot(kind='scatter', x=feature, y='PTS', ax=axs[index], figsize=(16, 3))

    
# line plot of points
NHL.PTS.plot()


# visualize correlation matrix in Seaborn using a heatmap
sns.heatmap(NHL.corr())
plt.savefig('heat_map.png') 


# calculate these metrics by hand!
from sklearn import metrics
import numpy as np


from sklearn.cross_validation import train_test_split

# define a function that accepts a list of features and returns testing RMSE
def train_test_rmse(feature_cols):
    X = NHL[feature_cols]
    y = NHL.PTS
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123)
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)
    y_pred = linreg.predict(X_test)
    return np.sqrt(metrics.mean_squared_error(y_test, y_pred))

# compare different sets of features
print train_test_rmse(['CF%', 'GF', 'Sh%', 'PDO'])


# split X and y into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123)

# create a NumPy array with the same shape as y_test
y_null = np.zeros_like(y_test, dtype=float)

# fill the array with the mean value of y_test
y_null.fill(y_test.mean())
y_null

# compute null RMSE
np.sqrt(metrics.mean_squared_error(y_test, y_null))


'''
Try a regression tree!
'''

feature_cols = ['CF%', 'GF', 'Sh%', 'PDO']
X = NHL[feature_cols]
y = NHL.PTS

# instantiate a DecisionTreeRegressor (with random_state=1)
from sklearn.tree import DecisionTreeRegressor
treereg = DecisionTreeRegressor(random_state=1)
treereg

# use leave-one-out cross-validation (LOOCV) to estimate the RMSE for this model
from sklearn.cross_validation import cross_val_score
scores = cross_val_score(treereg, X, y, cv=14, scoring='mean_squared_error')
np.mean(np.sqrt(-scores))


# list of values to try
max_depth_range = range(1, 8)

# list to store the average RMSE for each value of max_depth
RMSE_scores = []

# use LOOCV with each value of max_depth
for depth in max_depth_range:
    treereg = DecisionTreeRegressor(max_depth=depth, random_state=1)
    MSE_scores = cross_val_score(treereg, X, y, cv=14, scoring='mean_squared_error')
    RMSE_scores.append(np.mean(np.sqrt(-MSE_scores)))
    
    # plot max_depth (x-axis) versus RMSE (y-axis)
plt.plot(max_depth_range, RMSE_scores)
plt.xlabel('max_depth')
plt.ylabel('RMSE (lower is better)')
plt.savefig('R.png') 

# max_depth=3 was best, so fit a tree using that parameter
treereg = DecisionTreeRegressor(max_depth=3, random_state=1)
treereg.fit(X, y)

# "Gini importance" of each feature: the (normalized) total reduction of error brought by that feature
pd.DataFrame({'feature':feature_cols, 'importance':treereg.feature_importances_})

# create a Graphviz file
from sklearn.tree import export_graphviz
export_graphviz(treereg, out_file='tree_vehicles.dot', feature_names=feature_cols)

# At the command line, run this to convert to PNG:
#   dot -Tpng tree_vehicles.dot -o tree_vehicles.png


'''
RANDOM FORESTS
'''

NHL.head()
# encode categorical variables as integers
NHL['Team'] = pd.factorize(NHL.Team)[0]
NHL['TOI'] = pd.factorize(NHL.TOI)[0]
NHL.head()

# define features: exclude career statistics (which start with "C") and the response (Salary)
feature_cols = NHL.columns.drop('PTS')
feature_cols

# define X and y
X = NHL[feature_cols]
y = NHL.PTS

# list of values to try for max_depth
max_depth_range = range(1, 21)

# list to store the average RMSE for each value of max_depth
RMSE_scores = []

# use 10-fold cross-validation with each value of max_depth
from sklearn.cross_validation import cross_val_score
for depth in max_depth_range:
    treereg = DecisionTreeRegressor(max_depth=depth, random_state=1)
    MSE_scores = cross_val_score(treereg, X, y, cv=10, scoring='mean_squared_error')
    RMSE_scores.append(np.mean(np.sqrt(-MSE_scores)))

# plot max_depth (x-axis) versus RMSE (y-axis)
plt.plot(max_depth_range, RMSE_scores)
plt.xlabel('max_depth')
plt.ylabel('RMSE (lower is better)')
plt.savefig('Depth.png') 

# show the best RMSE and the corresponding max_depth
sorted(zip(RMSE_scores, max_depth_range))[0]

# max_depth=2 was best, so fit a tree using that parameter
treereg = DecisionTreeRegressor(max_depth=2, random_state=1)
treereg.fit(X, y)

# compute feature importances
pd.DataFrame({'feature':feature_cols, 'importance':treereg.feature_importances_}).sort('importance')

from sklearn.ensemble import RandomForestRegressor
rfreg = RandomForestRegressor()
rfreg

# tuning n_estimators

# list of values to try for n_estimators
estimator_range = range(10, 310, 10)

# list to store the average RMSE for each value of n_estimators
RMSE_scores = []

# use 5-fold cross-validation with each value of n_estimators (WARNING: SLOW!)
for estimator in estimator_range:
    rfreg = RandomForestRegressor(n_estimators=estimator, random_state=1)
    MSE_scores = cross_val_score(rfreg, X, y, cv=5, scoring='mean_squared_error')
    RMSE_scores.append(np.mean(np.sqrt(-MSE_scores)))
    
# plot n_estimators (x-axis) versus RMSE (y-axis)
plt.plot(estimator_range, RMSE_scores)
plt.xlabel('n_estimators')
plt.ylabel('RMSE (lower is better)')
plt.savefig('Estimators.png') 


# turning max features

# list of values to try for max_features
feature_range = range(1, len(feature_cols)+1)

# list to store the average RMSE for each value of max_features
RMSE_scores = []

# use 10-fold cross-validation with each value of max_features (WARNING: SLOW!)
for feature in feature_range:
    rfreg = RandomForestRegressor(n_estimators=150, max_features=feature, random_state=1)
    MSE_scores = cross_val_score(rfreg, X, y, cv=10, scoring='mean_squared_error')
    RMSE_scores.append(np.mean(np.sqrt(-MSE_scores)))
    
# plot max_features (x-axis) versus RMSE (y-axis)
plt.plot(feature_range, RMSE_scores)
plt.xlabel('max_features')
plt.ylabel('RMSE (lower is better)')
plt.savefig('Max_Features.png') 


# show the best RMSE and the corresponding max_features
sorted(zip(RMSE_scores, feature_range))[0]

# max_features=7 is best and n_estimators=150 is sufficiently large
rfreg = RandomForestRegressor(n_estimators=150, max_features=7, oob_score=True, random_state=1)
rfreg.fit(X, y)

# compute feature importances
pd.DataFrame({'feature':feature_cols, 'importance':rfreg.feature_importances_}).sort('importance')

# compute the out-of-bag R-squared score
rfreg.oob_score_

# check the shape of X
X.shape

# set a threshold for which features to include
print rfreg.transform(X, threshold=0.1).shape
print rfreg.transform(X, threshold='mean').shape
print rfreg.transform(X, threshold='median').shape

# create a new feature matrix that only includes important features
X_important = rfreg.transform(X, threshold='mean')

# check the RMSE for a Random Forest that only includes important features
rfreg = RandomForestRegressor(n_estimators=150, max_features=3, random_state=1)
scores = cross_val_score(rfreg, X_important, y, cv=10, scoring='mean_squared_error')
np.mean(np.sqrt(-scores))

'''
Redo KNN with Scalar Values
'''

# create feature matrix (X)
feature_cols = ['GF%', 'CF%', 'PDO']
X = NHL[feature_cols]

# create response vector (y)
y = NHL.PTS

# KNN with K=1
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X, y)

# standardize the features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)

# original values
X.values

# standardized values
X_scaled

# split into training and testing sets
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

# standardize X_train
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)

# standardize X_test
X_test_scaled = scaler.transform(X_test)

# check for correct standardization
print X_test_scaled[:, 0].mean()
print X_test_scaled[:, 0].std()
print X_test_scaled[:, 1].mean()
print X_test_scaled[:, 1].std()

# KNN accuracy on original data
knn = KNeighborsClassifier(n_neighbors=50)
knn.fit(X_train, y_train)
y_pred_class = knn.predict(X_test)
from sklearn import metrics
print metrics.accuracy_score(y_test, y_pred_class)

# KNN accuracy on scaled data
knn.fit(X_train_scaled, y_train)
y_pred_class = knn.predict(X_test_scaled)
print metrics.accuracy_score(y_test, y_pred_class)

'''
DB Scan Clustering
'''

# DBSCAN with eps=1 and min_samples=3
from sklearn.cluster import DBSCAN
db = DBSCAN(eps=1, min_samples=3)
db.fit(X_scaled)

# review the cluster labels
db.labels_

# save the cluster labels and sort by cluster
NHL['cluster'] = db.labels_
NHL.sort('cluster')

# review the cluster centers
NHL.groupby('cluster').mean()

# scatter plot matrix of DBSCAN cluster assignments (0=red, 1=green, 2=blue, -1=yellow)
pd.scatter_matrix(X, c=colors[NHL.cluster], figsize=(10,10), s=100)