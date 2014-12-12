_author_ = "Keerti Sekhar Sahoo"
import sys
from sklearn import datasets
from sklearn import cross_validation
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import KFold
import ast
#This implementation is to test whether a higher valued feature increases or decreases the chances of winning a game.
#This pre-processing helped in making a decision for the binary split for Decision Tree implementation.
data_file = "datadump.txt"
txt = open(data_file)
data = []
#queueType = 'NORMAL_5x5_BLIND'
#queueType = 'ARAM_5x5'
queueType = "ALL"
for i,dat in enumerate(txt):
    dat = ast.literal_eval(dat)
    if dat['queueType'] == queueType:
        dat = str(dat)
        data.append(dat)
    elif queueType == 'ALL':
        dat = str(dat)
        data.append(dat)
continuousFeaturesList = ['item3']
count = 0
counter =0
matches = len(data)
for i in range(0,matches):
    singleMatch = ast.literal_eval(data[i])
    tempList = []
    feature = continuousFeaturesList[0]
    for t in range(0,2):
        featureValueSum = 0.0
        if t ==0:
            start=0
            end=5
        else:
            start=5
            end=10
        for p in range(start,end):
            try:
                featureValue = singleMatch['participants'][p]['stats'][feature]
                featureValueSum += featureValue
            except IndexError:
                count +=1
            except KeyError:
                pass
        tempList.append(featureValueSum)
        print("Team",t,"'feature value sum is:",featureValueSum)
    #print("templist",tempList)
    #sys.exit(0)
    if singleMatch['teams'][0]['winner'] == True:
        print("Team 1 won")
        if tempList[0] > tempList[1]: #checking whether team1's total value more than team2
            print("True Positive")
            counter +=1
    else:
        print("Team 2 won")
        if tempList[1] > tempList[0]:
            print("True Positive")
            counter +=1

print("Total no of matches",matches)
print("No of counts based on higher total value = win:",counter)
print("Out of ", matches, "matches, for",counter,"matches, the team with high feature value sum wins the game.")




































