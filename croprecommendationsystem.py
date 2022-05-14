# -*- coding: utf-8 -*-
"""CropRecommendationSystem.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YsdoL8fVtmE6ucjObzRciSWIH-BfnDbd

# CROP RECOMMENDATION SYSTEM

# About the data

This data is relatively simple with very few but useful features unlike the complicated features affecting the yield of the crop.

The data have Nitrogen, Phosphorous, Pottasium and pH values of the soil. Also, it also contains the humidity, temperature and rainfall required for a particular crop.
"""

# Importing libraries

from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn import tree
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

! pip install kaggle

! mkdir ~/.kaggle
! cp /content/kaggle.json ~/.kaggle/
! chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d atharvaingle/crop-recommendation-dataset

!unzip /content/crop-recommendation-dataset.zip

PATH = '/content/Crop_recommendation.csv'
df = pd.read_csv(PATH)

df.head()

df.tail()

df.size

df.shape

df.columns

df['label'].unique()

df.dtypes

df['label'].value_counts()

print('Summer Crops:', df[(df['temperature']>30) & (df['humidity']>50)]['label'].unique())
print('Winter Crops:', df[(df['temperature']<20) & (df['humidity']>30)]['label'].unique())
print('Rainy Crops:', df[(df['rainfall']>200) & (df['humidity']>30)]['label'].unique())

plt.figure(figsize=(15, 28))
plt.subplot(4,2,1)
sns.barplot(df['N'], df['label'])
plt.ylabel(' ')
plt.xlabel('Nitrogen')
plt.subplot(4,2,2)
sns.barplot(df['P'], df['label'])
plt.ylabel(' ')
plt.xlabel('Phophorus')
plt.subplot(4,2,3)
sns.barplot(df['K'], df['label'])
plt.ylabel(' ')
plt.xlabel('Potassium')
plt.subplot(4,2,4)
sns.barplot(df['temperature'], df['label'])
plt.ylabel(' ')
plt.xlabel('Temperature')
plt.subplot(4,2,5)
sns.barplot(df['humidity'], df['label'])
plt.ylabel(' ')
plt.xlabel('Humidity')
plt.subplot(4,2,6)
sns.barplot(df['ph'], df['label'])
plt.ylabel(' ')
plt.xlabel('pH')
plt.subplot(4,2,7)
sns.barplot(df['rainfall'], df['label'])
plt.ylabel(' ')
plt.xlabel('rainfall')

plt.figure(figsize=(12,5))
plt.subplot(1, 2, 1)
# sns.distplot(df_setosa['sepal_length'],kde=True,color='green',bins=20,hist_kws={'alpha':0.3})
sns.distplot(df['temperature'],color="red",bins=15,hist_kws={'alpha':0.5})
plt.subplot(1, 2, 2)
sns.distplot(df['ph'],color="green",bins=15,hist_kws={'alpha':0.5})

sns.pairplot(df,hue = 'label')

sns.jointplot(x="rainfall",y="humidity",data=df[(df['temperature']<40) & 
                                                  (df['rainfall']>40)],height=10,hue="label")

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(30,15))
sns.boxplot(x='label',y='ph',data=df)

fig, ax = plt.subplots(1, 1, figsize=(15, 9))
sns.heatmap(df.corr(), annot=True,cmap='viridis')
ax.set(xlabel='features')
ax.set(ylabel='features')

plt.title('Correlation between different features', fontsize = 15, c='black')
plt.show()

df_summary = pd.pivot_table(df,index=['label'],aggfunc='mean')
df_summary.head()

fig = go.Figure()
fig.add_trace(go.Bar(
    x=df_summary.index,
    y=df_summary['N'],
    name='Nitrogen',
    marker_color='mediumvioletred'
))
fig.add_trace(go.Bar(
    x=df_summary.index,
    y=df_summary['P'],
    name='Phosphorous',
    marker_color='springgreen'
))
fig.add_trace(go.Bar(
    x=df_summary.index,
    y=df_summary['K'],
    name='Potash',
    marker_color='dodgerblue'
))

fig.update_layout(title="N-P-K values comparision between crops",
                  plot_bgcolor='white',
                  barmode='group',
                  xaxis_tickangle=-45)

fig.show()

"""### Seperating features and target label"""

features = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
target = df['label']
labels = df['label']

# Initializing empty lists to append all model's name and corresponding name
acc = []
model = []

# Splitting into train and test data

from sklearn.model_selection import train_test_split
Xtrain, Xtest, Ytrain, Ytest = train_test_split(features,target,test_size = 0.2,random_state =2)

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()

knn.fit(Xtrain,Ytrain)

predicted_values = knn.predict(Xtest)

x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('K Nearest Neighbours')
print("KNN Accuracy is: ", x)

print(classification_report(Ytest,predicted_values))

score = cross_val_score(knn,features,target,cv=5)
print('Cross validation score: ',score)

knn_train_accuracy = knn.score(Xtrain,Ytrain)
print("knn_train_accuracy = ",knn.score(Xtrain,Ytrain))
#Print Test Accuracy
knn_test_accuracy = knn.score(Xtest,Ytest)
print("knn_test_accuracy = ",knn.score(Xtest,Ytest))

score

Ypred = knn.predict(Xtest)
Ytrue = Ytest

from sklearn.metrics import confusion_matrix

cm_knn = confusion_matrix(Ytrue,Ypred)

f, ax = plt.subplots(figsize=(10,10))
sns.heatmap(cm_knn, annot=True, linewidth=0.5, fmt=".0f",cmap='viridis', ax = ax)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Predicted vs actual')
plt.show()

mean_acc = np.zeros(20)
for i in range(1,21):
    #Train Model and Predict  
    knn = KNeighborsClassifier(n_neighbors = i).fit(Xtrain,Ytrain)
    yhat= knn.predict(Xtest)
    mean_acc[i-1] = metrics.accuracy_score(Ytest, yhat)

mean_acc

loc = np.arange(1,21,step=1.0)
plt.figure(figsize = (10, 6))
plt.plot(range(1,21), mean_acc)
plt.xticks(loc)
plt.xlabel('Number of Neighbors ')
plt.ylabel('Accuracy')
plt.show()

from sklearn.model_selection import GridSearchCV
grid_params = { 'n_neighbors' : [12,13,14,15,16,17,18],
               'weights' : ['uniform','distance'],
               'metric' : ['minkowski','euclidean','manhattan']}

gs = GridSearchCV(KNeighborsClassifier(), grid_params, verbose = 1, cv=3, n_jobs = -1)

g_res = gs.fit(Xtrain, Ytrain)

g_res.best_score_

g_res.best_params_

# Using the best hyperparameters
knn_1 = KNeighborsClassifier(n_neighbors = 12, weights = 'distance',algorithm = 'brute',metric = 'manhattan')
knn_1.fit(Xtrain, Ytrain)

# Training & Testing accuracy after applying hyper parameter
knn_train_accuracy = knn_1.score(Xtrain,Ytrain)
print("knn_train_accuracy = ",knn_1.score(Xtrain,Ytrain))
#Print Test Accuracy
knn_test_accuracy = knn_1.score(Xtest,Ytest)
print("knn_test_accuracy = ",knn_1.score(Xtest,Ytest))

"""# My first Model Decision Tree"""

from sklearn.tree import DecisionTreeClassifier

DecisionTree = DecisionTreeClassifier(criterion="entropy",random_state=2,max_depth=5)

DecisionTree.fit(Xtrain,Ytrain)

predicted_values = DecisionTree.predict(Xtest)
x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('Decision Tree')
print("DecisionTrees's Accuracy is: ", x*100)

print(classification_report(Ytest,predicted_values))

from sklearn.model_selection import cross_val_score

# Cross validation score (Decision Tree)
score = cross_val_score(DecisionTree, features, target,cv=5)

DecisionTree_accuracy = DecisionTree.score(Xtrain,Ytrain)
print("DecisionTree_train_accuracy = ",DecisionTree.score(Xtrain,Ytrain))
#Print Test Accuracy
DecisionTree_test_accuracy = DecisionTree.score(Xtest,Ytest)
print("DecisionTree_test_accuracy = ",DecisionTree.score(Xtest,Ytest))

score

Ypred = DecisionTree.predict(Xtest)
Ytrue = Ytest

from sklearn.metrics import confusion_matrix

cm_DecisionTree = confusion_matrix(Ytrue,Ypred)

f, ax = plt.subplots(figsize=(10,10))
sns.heatmap(cm_DecisionTree, annot=True, linewidth=0.5, fmt=".0f",  cmap='viridis', ax = ax)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title('Predicted vs actual')
plt.show()

"""### Saving trained Decision Tree model"""

import pickle
# Dump the trained Naive Bayes classifier with Pickle
DT_pkl_filename = 'DecisionTree.pkl'
# Open the file to save as pkl file
DT_Model_pkl = open(DT_pkl_filename, 'wb')
pickle.dump(DecisionTree, DT_Model_pkl)
# Close the pickle instances
DT_Model_pkl.close()

"""# Guassian Naive Bayes"""

from sklearn.naive_bayes import GaussianNB

NaiveBayes = GaussianNB()

NaiveBayes.fit(Xtrain,Ytrain)

predicted_values = NaiveBayes.predict(Xtest)
x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('Naive Bayes')
print("Naive Bayes's Accuracy is: ", x)

print(classification_report(Ytest,predicted_values))

# Cross validation score (NaiveBayes)
score = cross_val_score(NaiveBayes,features,target,cv=5)
score

"""### Saving trained Guassian Naive Bayes model"""

import pickle
# Dump the trained Naive Bayes classifier with Pickle
NB_pkl_filename = 'NBClassifier.pkl'
# Open the file to save as pkl file
NB_Model_pkl = open(NB_pkl_filename, 'wb')
pickle.dump(NaiveBayes, NB_Model_pkl)
# Close the pickle instances
NB_Model_pkl.close()

"""# Support Vector Machine (SVM)"""

from sklearn.svm import SVC

SVM = SVC(gamma='auto')

SVM.fit(Xtrain,Ytrain)

predicted_values = SVM.predict(Xtest)

x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('SVM')
print("SVM's Accuracy is: ", x)

print(classification_report(Ytest,predicted_values))

# Cross validation score (SVM)
score = cross_val_score(SVM,features,target,cv=5)
score

"""# Logistic Regression"""

from sklearn.linear_model import LogisticRegression

LogReg = LogisticRegression(random_state=2)

LogReg.fit(Xtrain,Ytrain)

predicted_values = LogReg.predict(Xtest)

x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('Logistic Regression')
print("Logistic Regression's Accuracy is: ", x)

print(classification_report(Ytest,predicted_values))

# Cross validation score (Logistic Regression)
score = cross_val_score(LogReg,features,target,cv=5)
score

"""### Saving trained Logistic Regression model"""

import pickle
# Dump the trained Naive Bayes classifier with Pickle
LR_pkl_filename = 'LogisticRegression.pkl'
# Open the file to save as pkl file
LR_Model_pkl = open(DT_pkl_filename, 'wb')
pickle.dump(LogReg, LR_Model_pkl)
# Close the pickle instances
LR_Model_pkl.close()

"""# Random Forest"""

from sklearn.ensemble import RandomForestClassifier

RF = RandomForestClassifier(n_estimators=20, random_state=0)
RF.fit(Xtrain,Ytrain)

predicted_values = RF.predict(Xtest)

x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('RF')
print("RF's Accuracy is: ", x)

print(classification_report(Ytest,predicted_values))

# Cross validation score (Random Forest)
score = cross_val_score(RF,features,target,cv=5)
score

"""### Saving trained Random Forest model"""

import pickle
# Dump the trained Naive Bayes classifier with Pickle
RF_pkl_filename = 'RandomForest.pkl'
# Open the file to save as pkl file
RF_Model_pkl = open(RF_pkl_filename, 'wb')
pickle.dump(RF, RF_Model_pkl)
# Close the pickle instances
RF_Model_pkl.close()

"""# XGBoost"""

import xgboost as xgb
XB = xgb.XGBClassifier()
XB.fit(Xtrain,Ytrain)

predicted_values = XB.predict(Xtest)

x = metrics.accuracy_score(Ytest, predicted_values)
acc.append(x)
model.append('XGBoost')
print("XGBoost's Accuracy is: ", x)

print(classification_report(Ytest,predicted_values))

# Cross validation score (XGBoost)
score = cross_val_score(XB,features,target,cv=5)
score

"""### Saving trained XGBoost model"""

import pickle
# Dump the trained Naive Bayes classifier with Pickle
XB_pkl_filename = 'XGBoost.pkl'
# Open the file to save as pkl file
XB_Model_pkl = open(XB_pkl_filename, 'wb')
pickle.dump(XB, XB_Model_pkl)
# Close the pickle instances
XB_Model_pkl.close()

"""## Accuracy Comparison"""

plt.figure(figsize=[10,5],dpi = 100)
plt.title('Accuracy Comparison')
plt.xlabel('Accuracy')
plt.ylabel('Algorithm')
sns.barplot(x = acc,y = model,palette='dark')

label = ['KNN', 'Decision Tree','Random Forest','Naive Bayes','XG Boost']
Test = [knn_test_accuracy, dt_test_accuracy,rf_test_accuracy,
        nb_test_accuracy, XB_test_accuracy]
Train = [knn_train_accuracy,  dt_train_accuracy, rf_train_accuracy,
         nb_train_accuracy, XB_train_accuracy]

f, ax = plt.subplots(figsize=(20,7)) # set the size that you'd like (width, height)
X_axis = np.arange(len(label))
plt.bar(X_axis - 0.2,Test, 0.4, label = 'Test', color=('midnightblue'))
plt.bar(X_axis + 0.2,Train, 0.4, label = 'Train', color=('mediumaquamarine'))

plt.xticks(X_axis, label)
plt.xlabel("ML algorithms")
plt.ylabel("Accuracy")
plt.title("Testing vs Training Accuracy")
plt.legend()
#plt.savefig('train vs test.png')
plt.show()

accuracy_models = dict(zip(model, acc))
for k, v in accuracy_models.items():
    print (k, '-->', v)

"""## Making a prediction"""

data = np.array([[104,18, 30, 23.603016, 60.3, 6.7, 140.91]])
prediction = RF.predict(data)
print(prediction)

data = np.array([[83, 45, 60, 28, 70.3, 7.0, 150.9]])
prediction = RF.predict(data)
print(prediction)