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
#queueType = 'RANKED_SOLO_5x5'
queueType = 'NORMAL_5x5_BLIND'
#queueType = 'ARAM_5x5'
#queueType = "MIXED"
for i,dat in enumerate(txt):
    dat = ast.literal_eval(dat)
    if dat['queueType'] == queueType:
        dat = str(dat)
        data.append(dat)
    elif queueType == 'MIXED':
        dat = str(dat)
        data.append(dat)
#Combine features of both teams and predict
binaryFeatures = ['firstInhibitor','firstBaron','firstDragon','firstTower','firstBlood']

continuousFeaturesList = ['baronKills','dragonKills']
# exceptionFeatureList is the one which contains the features those with higher
exceptionFeatureList = ['deaths','magicDamageTaken','physicalDamageTaken','totalDamageTaken',
                        'visionWardsBoughtInGame','wardsKilled','wardsPlaced']

X = []
Y = []
for i in range(0,len(data)):
    singleMatch = ast.literal_eval(data[i])
    teamsTotalValueList = []
    '''For Team 1 and Team 2'''
    tempList = []
    if len(binaryFeatures) > 0:
        for t in range(0,2):
            '''Training for binary features  '''
            for f in range(0,len(binaryFeatures)):
                feature = binaryFeatures[f]
                featureValue = singleMatch['teams'][t][feature]
                tempList.append(featureValue)

    '''Training for continuous feature values '''
    if len(continuousFeaturesList) > 0:
        for i in range(0,len(continuousFeaturesList)):
            feature = continuousFeaturesList[i]
            for t in range(0,2):
                featureValueSum = 0
                if t==0:
                    for i in range(0,5):
                        try:
                            featureValueSum = singleMatch['participants'][i]['stats'][feature] # i =0 means player1
                        except IndexError:
                            pass
                        except KeyError:
                            pass
                    teamsTotalValueList.append(featureValueSum)
                if t==1:
                    for i in range(5,10):
                        try:
                            featureValueSum = singleMatch['participants'][i]['stats'][feature] # i =5 means player5
                        except IndexError:
                            pass
                        except KeyError:
                            pass
                    teamsTotalValueList.append(featureValueSum)
            if teamsTotalValueList[0] > teamsTotalValueList[1] and feature not in exceptionFeatureList: #check if team 1 has greater total value than team 2
                tempList.append(1)
            elif teamsTotalValueList[1] > teamsTotalValueList[0] and feature not in exceptionFeatureList:
                tempList.append(1)
            else:
                tempList.append(0)
    if singleMatch['teams'][0]['winner'] == True:
        result = 'T1'
    else:
        result = 'T2'
    Y.append(result)
    X.append(tempList)

X = np.array(X)
Y = np.array(Y)
dctAccuracyList = []
acc_total = 0

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
    acc_total+=accuracy

    print("Decision tree accuracy is:",accuracy)

print('acc total: ', acc_total/10)









