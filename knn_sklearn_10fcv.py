#author: Mitchel Hally
#using Sklearn's KNN classifier
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
import matplotlib.pyplot as plt
import ast
from random import shuffle
import numpy as np
import math
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import KFold
from sklearn.preprocessing import MinMaxScaler as mms
import pydot #attempted using pydot to show a graph of feature representation

def loadJsonFile(file):

    jsonData = open(file)
    data = []

    for index, json in enumerate(jsonData):
        dictMatch = ast.literal_eval(json)
        data.append(dictMatch)

    shuffle(data)
    return data

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
    # if match['queueType'] == 'NORMAL_5x5_BLIND' or match['queueType'] == 'RANKED_SOLO_5x5':
    if match['queueType'] == 'RANKED_SOLO_5x5':
        for info in match:
            #match contains team info amonst other things like date, map, season, etc.
            winner_team = -1
            temp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            #create feature set, each feature once for each team
            for team_index , team_info in enumerate(match['teams']):
                for team in team_info:
                    if team == 'firstTower':
                        temp[0+team_index] = team_info[team]
                    if team == 'firstBlood':                     
                        temp[2+team_index] = team_info[team]
                    if team == 'firstBaron' :                     
                        temp[4+team_index] = team_info[team]
                    if team  == 'firstInhibitor':                     
                        temp[6+team_index] = team_info[team]
                    if team == 'firstDragon':
                        temp[8+team_index] = team_info[team]
                    if team == 'baronKills':                     
                        temp[10+team_index] = team_info[team]
                    if team == 'dragonKills':
                        temp[12+team_index] = team_info[team]
                    #"cheating features"
                    # if team == 'towerKills':
                    #     temp[14+team_index] = team_info[team]
                    # if team == 'inhibitorKills':
                    #     temp[16+team_index] = team_info[team] 
                    if team == 'winner' and team_info[team]:
                        winner_team = team_index
                  
            teams['data'].append(temp)
            teams['label'].append(winner_team)

# #some eda
# games = 0
# wins = 0
# team1t = 0
# team2t = 0
# team1i = 0
# team2i = 0
# team1b = 0
# team2b = 0
# team1d = 0
# team2d = 0
# for i in teams['label']:
#     games+=1
#     if (i==1):
#         wins+=1

# for d in teams['data']:
#     team1t += d[0]
#     team2t += d[1]
#     team1i += d[2]
#     team2i += d[3]
#     team1b += d[4]
#     team2b += d[5]
#     team1d += d[6]
#     team2d += d[7]

# t2 = float(wins)/float(games)
# t1wins = games-wins
# t1 = float(t1wins)/float(games)
# print 'Team 1 won', int(t1*100), '% of the ', games, ' games!'
# print 'towers: ', team1t, 'inhibitors:', team1i, 'barons: ', team1b, 'dragons: ', team1d, '\n'
# print 'Team 2 won', int(t2*100), '% of the ', games,' games!'
# print 'towers: ', team2t, 'inhibitors:', team2i, 'barons: ', team2b, 'dragons: ', team2d, '\n'

kf = KFold(len(teams['data']), n_folds=10)
X = np.array(teams['data'])
Y = np.array(teams['label'])
mimas = mms()
i = 0
max_acc = 0
max_k = 0
for k in range(20):
    acc = 0
    for train, test in kf:
        if (k>0):
            X_train, X_test, y_train, y_test = X[train], X[test], Y[train], Y[test]
            scaler = mimas.fit(X_train)
            scaler_train = scaler.transform(X_train)
            scaler_test = scaler.transform(X_test)
            i+=1
            kn = KNeighborsClassifier(n_neighbors=k)
            # kn.fit(X_train, y_train)
            kn.fit(scaler_train, y_train)
            labels_pred = kn.predict(scaler_test)
            labels_pred = kn.predict(X_test)
            labels_true = y_test
            my_acc = kn.score(scaler_train, y_train)
            # my_acc = kn.score(X_train, y_train)
            acc += my_acc
    print 'k:',k,' 10-fold accuracy: ', acc/10
    if k==2:
        max_acc = acc/10
        max_k = k
    if (acc/10) > max_acc:    
        max_acc = acc/10
        max_k = k

print 'k:',max_k,' 10-fold accuracy: ', max_acc

