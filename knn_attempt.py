#author: Mitchel Hally
#I am working on another version based off the tutorial from the knn slides
#from the DM class and believe I will find more success as I understand the data a lot more
#now than when I first implemented this
import operator
from sklearn import metrics
import matplotlib.pyplot as plt
import ast
from random import shuffle
import numpy as np
import math
from sklearn.cross_validation import KFold
from sklearn.preprocessing import MinMaxScaler as mms

def euclideanDistance(v1, v2):

    return ((v1-v2)**2).sum()

def knn(k, train, test):
    all_dist = []
    for x_index, index in enumerate(train):
        my_dist = euclideanDistance(test, train[x_index])
        all_dist.append((train[x_index], my_dist))
    all_dist.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(all_dist[x][0])

    return neighbors

def vote(neighbors):
    votes = {}
    for x_index, x in enumerate(neighbors):
        vote = neighbors[x_index][-1]
        if vote in votes:
            votes[vote] += 1
        else:
            votes[vote] = 1
    sort = sorted(votes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sort[0][0]

def calculateAccuracy(test, guesses):
    correct = 0
    for x_index, x in enumerate(test):
        if test[x_index][-1] == guesses[x_index]:
            correct += 1
    return (correct/float(len(test))) * 100.0

def loadJsonFile(file):

    jsonData = open(file)
    data = []

    for index, json in enumerate(jsonData):
        dictMatch = ast.literal_eval(json)
        data.append(dictMatch)

    shuffle(data)
    return data

if __name__ == '__main__':
    teams={}
    teams['data'] = []
    teams['label'] = []
    players={}
    players['data'] = []
    players['label'] = []
    #Agreement : if team2>team1 label == true;
    # firstTower, firstBlood, firstBaron, firstInhibitor, firstDragon
    data = loadJsonFile('datadump.txt')
    for match in data:
        #each match has several queue types, mainly focused on two most played
        if match['queueType'] == 'NORMAL_5x5_BLIND' or match['queueType'] == 'RANKED_SOLO_5x5':
        # if match['queueType'] == 'NORMAL_5x5_BLIND':
            for info in match:
                #match contains team info amonst other things like date, map, season, etc.
                winner_team = -1
                temp = [0,0,0,0,0,0,0,0]
                #create feature set, each feature once for each team
                for team_index , team_info in enumerate(match['teams']):
                    for team in team_info:
                        # if team == 'firstTower':
                        #     temp[0+team_index] = team_info[team]
                        # if team == 'firstBlood':                     
                        #     temp[2+team_index] = team_info[team]
                        # if team == 'firstBaron' :                     
                        #     temp[4+team_index] = team_info[team]
                        # if team  == 'firstInhibitor':                     
                        #     temp[6+team_index] = team_info[team]
                        # if team == 'firstDragon':
                        #     temp[8+team_index] = team_info[team]
                        if team == 'baronKills':                     
                            temp[0+team_index] = team_info[team]
                        if team == 'dragonKills':
                            temp[2+team_index] = team_info[team]
                        #"cheating features"
                        if team == 'towerKills':
                            temp[4+team_index] = team_info[team]
                        if team == 'inhibitorKills':
                            temp[6+team_index] = team_info[team] 
                        if team == 'winner' and team_info[team]:
                            winner_team = team_index
                      
                teams['data'].append(temp)
                teams['label'].append(winner_team)

    kf = KFold(len(teams['data']), n_folds=10)
    X = np.array(teams['data'])
    Y = np.array(teams['label'])
    mimas = mms()
    i = 0
    max_acc = 0
    max_k = 0
    k = 8
    acc_total = 0
    for train, test in kf:
        X_train, X_test, y_train, y_test = X[train], X[test], Y[train], Y[test]
        guesses = []
        # scaler = mimas.fit(X_train)
        # scaler_train = scaler.transform(X_train)
        # scaler_test = scaler.transform(X_test)        
        i+=1
        for x in range(len(X_test)):
            neighbors = knn(k, X_train, X_test)
            votes = vote(neighbors)
            guesses.append(votes)
        acc = calculateAccuracy(X_test, guesses)
        acc_total+=acc
        print 'fold', i, 'accuracy', acc

    tenfold = acc_total/10
    print '10-fold Accuracy', tenfold
