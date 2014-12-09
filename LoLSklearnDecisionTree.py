_author_ = "Keerti Sekhar Sahoo"
import sys
from sklearn import datasets
from sklearn import cross_validation
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import KFold
import ast

data_file = "datadump.txt"
txt = open(data_file)
data = []
for i,dat in enumerate(txt):
    data.append(dat)

featureList = ['firstBlood','firstTower','firstBaron','firstBlood','firstBaron']
X = []
Y = []
for i in range(0,len(data)):
    singleMatch = ast.literal_eval(data[i])
    '''For Team 1 and Team 2'''
    tempList = []
    for t in range(0,2):
        for f in range(0,len(featureList)):
            feature = featureList[f]
            featureValue = singleMatch['teams'][t][feature]
            tempList.append(featureValue)
    if singleMatch['teams'][0]['winner'] == True:
        result = 'T1'
    else:
        result = 'T2'
    Y.append(result)
    X.append(tempList)

X = np.array(X)
Y = np.array(Y)
dctAccuracyList = []

kf = KFold(len(X), n_folds = 10)
for train, test in kf:
    X_train = X[train]
    Y_train = Y[train]
    X_test = X[test]
    Y_test = Y[test]

''' Decision tree implementation '''
dtc = DecisionTreeClassifier()
dtc = dtc.fit(X_train,Y_train)
dtc = dtc.predict(X_test)
correct = 0.0
for i in range(0,len(Y_test)):
    if Y_test[i] == dtc[i]:
        correct +=1
accuracy = (float)(correct/len(Y_test))* (100)
dctAccuracyList.append(accuracy)

print("Decision tree accuracy is:",dctAccuracyList)








