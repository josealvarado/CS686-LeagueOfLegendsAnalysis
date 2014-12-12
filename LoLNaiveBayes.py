_author_ = "Keerti Sekhar Sahoo"
import json
import sys
import ast
import math
from sklearn.cross_validation import KFold
class LeagueOfLegends:
    def __init__(self):
        self.varianceDictT1 = {} # Dict for storing variance of all the features when y is Y1
        self.varianceDictT2 = {} # Dict for storing variance of all the features when y is Y2
        self.meanDictT1 = {}
        self.meanDictT2 = {}
        self.priorProbT1 = 0.0
        self.priorProbT2 = 0.0
        self.data = []
        self.truthList = []
        self.guessList = []
        self.trainingData = []
        self.testData = []
        self.continuousFeatures = []
        self.binaryFeatures = []
        self.binaryFeatProbDictT1 = {} # Stores the probabilities of binary features when Team1 wins
        self.binaryFeatProbDictT2 = {} # e.g. {firstBlood : {True: prob,False:prob}}

    def readData(self):
        data_file = "datadump.txt"
        txt = open(data_file)
        data = self.data # Data about all the matches
        #queueType = 'NORMAL_5x5_BLIND'
        #queueType = 'ARAM_5x5'
        queueType = "MIXED"
        for i,dat in enumerate(txt):
            dat = ast.literal_eval(dat)
            if dat['queueType'] == queueType:
                dat = str(dat)
                data.append(dat)
            elif queueType == 'MIXED':
                dat = str(dat)
                data.append(dat)

    def trainLoLModel(self):
        #print("hello")
        data = self.data
        '''Divide the data into training and test sets '''
        trainingData = self.trainingData
        testData = self.testData
        kf = KFold(len(data),n_folds = 5)
        for train,test in kf:
            for index in train:
                trainingData.append(data[index])
            for index in test:
                testData.append(data[index])
            break
        print("Length of training set is:",len(trainingData),"and length of test set is:",len(testData))

        ''' Declare the feature list '''
        continuousFeatures = self.continuousFeatures
        binaryFeatures = self.binaryFeatures
        # featureList = ['physicalDamageTaken', 'neutralMinionsKilled', 'inhibitorKills', 'neutralMinionsKilledEnemyJungle',
        #                'magicDamageDealtToChampions', 'towerKills', 'goldSpent', 'doubleKills', 'killingSprees','firstBloodKill']

        binaryFeatures = ['firstInhibitor','firstTower','firstBaron','firstBlood','firstDragon']
        continuousFeatures = ['towerKills','inhibitorKills','baronKills','dragonKills']

        self.continuousFeatures = continuousFeatures
        ''' Count of no of time Team1 winning and Team2 winning '''
        teamOneWinCount = 0
        teamTwoWinCount = 0
        for i in range(0,len(trainingData)):
            singleMatch = ast.literal_eval(trainingData[i])
            if singleMatch['teams'][0]['winner'] == True:
                teamOneWinCount+=1
            else:
                teamTwoWinCount+=1
        print "Team1 wins",teamOneWinCount,"times and Team2 wins",teamTwoWinCount,"times" # 373 and 297

        ''' Calculate the prior probabilities '''
        priorProbT1 = (float)(teamOneWinCount)/(float)(len(trainingData)) # change the len back to no of matches
        priorProbT2 = (float)(teamTwoWinCount)/(float)(len(trainingData))
        self.priorProbT1 = priorProbT1
        self.priorProbT2 = priorProbT2
        #print(priorProbT1,priorProbT2)

        '''Calculate no of occurrences of the binary features in the training data '''
        binaryFeatProbDictT1 = self.binaryFeatProbDictT1
        binaryFeatProbDictT2 = self.binaryFeatProbDictT2
        for f in range(0,len(binaryFeatures)):
            feature = binaryFeatures[f]
            print(feature)
            binaryFeatProbDictT1[feature] = {}
            binaryFeatProbDictT2[feature] = {}
            for i in range(0,len(trainingData)):
                #print(i)
                singleMatch = ast.literal_eval(trainingData[i])
                if singleMatch['teams'][0]['winner'] == True: # TEAM 1 wins
                    if singleMatch['teams'][0][feature] == True:
                        try:
                            binaryFeatProbDictT1[feature]['True'] += 1
                        except KeyError:
                            binaryFeatProbDictT1[feature]['True'] = 1
                    else:
                        try:
                            binaryFeatProbDictT1[feature]['False'] += 1
                        except KeyError:
                            binaryFeatProbDictT1[feature]['False'] = 1
                else:
                    if singleMatch['teams'][1][feature] == True:
                        try:
                            binaryFeatProbDictT2[feature]['True'] += 1
                        except KeyError:
                            binaryFeatProbDictT2[feature]['True'] = 1
                    else:
                        try:
                            binaryFeatProbDictT2[feature]['False'] += 1
                        except KeyError:
                            binaryFeatProbDictT2[feature]['False'] = 1
            try:
                binaryFeatProbDictT1[feature]['True'] = (float)(binaryFeatProbDictT1[feature]['True'])/(float)(teamOneWinCount)
            except KeyError:
                pass
            try:
                binaryFeatProbDictT1[feature]['False'] = (float)(binaryFeatProbDictT1[feature]['False'])/(float)(teamOneWinCount)
            except KeyError:
                pass
            try:
                binaryFeatProbDictT2[feature]['True'] = (float)(binaryFeatProbDictT2[feature]['True'])/(float)(teamTwoWinCount)
            except KeyError:
                pass
            try:
                binaryFeatProbDictT2[feature]['False'] = (float)(binaryFeatProbDictT2[feature]['False'])/(float)(teamTwoWinCount)
            except KeyError:
                pass
        #print("binT1",binaryFeatProbDictT1)
        #print("binT2",binaryFeatProbDictT2)
        #sys.exit(0)

        ''' Calculate Gaussian mean for all the continuous features when y is Y1(Team1 wins) and Y2(Team2 wins)'''
        meanDictT1 = self.meanDictT1 # dict for storing mean values of all the features when Y1
        meanDictT2 = self.meanDictT2 # dict for storing mean values of all the features when Y2

        teamOneFeatureValueSumDict = {} # list with data about team1's sum of featureValues for each match
        teamTwoFeatureValueSumDict = {}
        #myList = []
        for i in range(0,len(continuousFeatures)): # Go through each feature
            feature = continuousFeatures[i]
            teamOneFeatureValue = 0
            teamTwoFeatureValue = 0

            teamOneFeatureValueSumDict[feature] = {}
            teamTwoFeatureValueSumDict[feature] = {}
            for m in range(0, len(trainingData)): # go through single match's data
                #print(m)
                #print("data",data[0])
                #sys.exit(0)
                teamOneSingleMatchFeatureValue = 0 # Team's sum of feature values for a single match and for specific feature
                teamTwoSingleMatchFeatureValue = 0
                #print("feature",feature)
                singleMatchDict = ast.literal_eval(trainingData[m]) # single match.dict
                #print(singleMatchDict)
                statusofTeamOneWins = singleMatchDict['teams'][0]['winner'] # whether Team1 won or lost
                participantsList = singleMatchDict['participants'] # details of all the participants of a match
                #print("len",len(participantsList))

                if statusofTeamOneWins == True:
                    #myList.append(1)
                    for p in range(0,5):
                        #print(participantsList[p]['stats'][feature]) # featureValue of a specific feature
                        try:
                            teamOneSingleMatchFeatureValue += participantsList[p]['stats'][feature]
                            teamOneFeatureValue += participantsList[p]['stats'][feature]
                        except KeyError: # To ignore the error in case data is unavailable for the feature
                            pass
                        except IndexError: # To ignore the error in case of unavailability of data for a participant
                            pass
                else:
                    #myList.append(0)
                    for p in range(5,10):
                        #print(participantsList[p]['stats'][feature])
                        try:
                            teamTwoSingleMatchFeatureValue += participantsList[p]['stats'][feature]
                            teamTwoFeatureValue += participantsList[p]['stats'][feature]
                        except KeyError:
                            pass
                        except IndexError:
                            pass
                ''' Storing individual match's sum of feature values for Team1 and Team2'''
                teamOneFeatureValueSumDict[feature][m] = teamOneSingleMatchFeatureValue
                teamTwoFeatureValueSumDict[feature][m] = teamTwoSingleMatchFeatureValue
            ''' Storing gaussian mean values for each feature for Y1 and Y2'''
            meanDictT1[feature] = teamOneFeatureValue / teamOneWinCount
            meanDictT2[feature] = teamTwoFeatureValue / teamTwoWinCount

        print("meanDictY1",meanDictT1)
        print("meanDictY2",meanDictT2)
        print("teamOneFeatureValueSum",teamOneFeatureValueSumDict)
        #print("myList",myList)
        print("teamTwoFeatureValueSum",teamTwoFeatureValueSumDict)
        ''' Calculate Gaussian variance for all the continuous features when y is Y1(Team1 wins) and Y2(Team2 wins) '''
        varianceDictY1 = self.varianceDictT1
        varianceDictY2 = self.varianceDictT2
        for f in range(0,len(continuousFeatures)):
            feature = continuousFeatures[f]
            teamOneVarianceSum = 0
            teamTwoVarianceSum = 0
            for i in range(0, len(trainingData)):
                if teamOneFeatureValueSumDict[feature][i] != 0:
                    teamOneVarianceSum += (teamOneFeatureValueSumDict[feature][i] - meanDictT1[feature])**2
                else:
                    teamTwoVarianceSum += (teamTwoFeatureValueSumDict[feature][i] - meanDictT2[feature])**2
            varianceDictY1[feature] = teamOneVarianceSum / teamOneWinCount
            varianceDictY2[feature] = teamTwoVarianceSum / teamTwoWinCount
        print('varianceDictY1',varianceDictY1)
        print('varianceDictY2',varianceDictY2)
        #sys.exit(0)

    def classify(self):
        print "Testing......."
        print"Inside Classify"
        testData = self.testData
        for m in range(0,len(testData)):
            predictLoL = self.calculateLogJointProbabilities(testData[m])
        print("truthList",self.truthList)
        print("guessList",self.guessList)
        ''' Count accuracy '''
        count = 0.0
        for i in range(0,len(self.truthList)):
            if self.truthList[i] == self.guessList[i]:
                count +=1
        print("Accuracy is ",count/len(testData))


    def calculateLogJointProbabilities(self,singleMatchData):
        print("Calculating log Joint Probabilities..........")
        #print(singleMatchData)
        singleMatchData = ast.literal_eval(singleMatchData)
        statusT1 = singleMatchData['teams'][0]['winner']
        statusT2 = singleMatchData['teams'][1]['winner']
        if statusT1 == True:
            self.truthList.append('T1')
        else:
            self.truthList.append('T2')
        #print("winStatus",winStatus)
        #sys.exit(0)
        #participantsList = singleMatchData['participants'][0]['stats']['killingSprees']
        #print(participantsList)
        #print("features",self.featureList)
        #result = ((float)(1)/(float)(2*math.pi*23))* (math.exp((-0.5) * ((float)(math.pow((10-11),2))/(float)(23))))
        posteriorProbListT1 = [] #Stores the probabilities of each feature for a single match when T1 wins
        posteriorProbListT2 = [] #Stores the probabilities of each feature for a single match when T2 wins
        ''' Considering T1 wins '''
        if len(self.continuousFeatures) > 0:
            for f in range(0,len(self.continuousFeatures)):
                feature = self.continuousFeatures[f]
                xValue = 0
                '''xValue when T1 wins, summation of all the feature values for each feature. first 5 players '''
                for i in range(0,5):
                    try:
                        xValue += singleMatchData['participants'][i]['stats'][feature]
                    except KeyError:
                        pass
                    except IndexError:
                        pass
                '''Posterior probability calculation when T1'''
                try:
                    posteriorProb = ((float)(1)/math.sqrt((float)(2*math.pi*self.varianceDictT1[feature]))) * (math.exp((-0.5) * ((float)(math.pow((xValue-self.meanDictT1[feature]),2))/(float)(self.varianceDictT1[feature]))))
                except KeyError:
                    pass
                except ZeroDivisionError:
                    posteriorProb = 1
                    #pass
                posteriorProbListT1.append(posteriorProb) # each posterior prob value is added to the list for single feature

        ''' Considering T2 wins '''
        if len(self.continuousFeatures) >0 :
            for f in range(0,len(self.continuousFeatures)):
                feature = self.continuousFeatures[f]
                xValue = 0
                '''xValue when T2 wins, summation of all the feature values for each feature. last 5 players '''
                for i in range(5,10):
                    try:
                        xValue += singleMatchData['participants'][i]['stats'][feature]
                    except KeyError:
                        pass
                    except IndexError:
                        pass
                '''Posterior probability calculation when T2 wins'''
                try:
                    posteriorProb = ((float)(1)/math.sqrt((float)(2*math.pi*self.varianceDictT2[feature]))) * (math.exp((-0.5) * ((float)(math.pow((xValue-self.meanDictT2[feature]),2))/(float)(self.varianceDictT2[feature]))))
                except KeyError:
                    pass
                except ZeroDivisionError:
                    posteriorProb = 1
                    #pass
                posteriorProbListT2.append(posteriorProb) # each posterior prob value is added to the list for single feature
        print("postProbListT1",posteriorProbListT1)
        print("postProbListT2",posteriorProbListT2)
        #print(self.priorProbT1)
        #print(self.priorProbT2)

        '''Calculating log joint probability for a single match considering T1 wins '''
        logJointProbT1 = 0.0
        ''' Probabilities for continuous features '''
        if len(self.continuousFeatures) > 0:
            for i in range(0,len(posteriorProbListT1)): # no of continuous features
                logJointProbT1 += math.log(posteriorProbListT1[i], 10)
        '''Probabilities for binary features '''
        if len(self.binaryFeatures) > 0:
            for i in range(0,len(self.binaryFeatures)): # no of binary features
                feature = self.binaryFeatures[i]
                if singleMatchData['teams'][0][feature] == True:
                    logJointProbT1 += math.log(self.binaryFeatProbDictT1[feature]['True'], 10)
                else:
                    logJointProbT1 += math.log(self.binaryFeatProbDictT1[feature]['False'], 10)
        logJointProbT1 += math.log(self.priorProbT1, 10)

        '''Calculating log joint probability for a single match considering T2 wins '''
        logJointProbT2 = 0.0
        ''' Probabilities for continuous features  '''
        if len(self.continuousFeatures) > 0:
            for i in range(0,len(posteriorProbListT2)): # no of continuous features
                logJointProbT2 += math.log(posteriorProbListT2[i], 10)
        '''Probabilities for binary features '''
        if len(self.binaryFeatures) > 0:
            for i in range(0,len(self.binaryFeatures)): # no of binary features
                feature = self.binaryFeatures[i]
                if singleMatchData['teams'][0][feature] == True:
                    logJointProbT2 += math.log(self.binaryFeatProbDictT2[feature]['True'], 10)
                else:
                    logJointProbT2 += math.log(self.binaryFeatProbDictT2[feature]['False'], 10)
        logJointProbT2 += math.log(self.priorProbT2, 10)
        print("logJointProbT1",logJointProbT1)
        print("logJointProbT2",logJointProbT2)
        if logJointProbT1 > logJointProbT2:
            #print("T1 wins")
            self.guessList.append('T1')
        else:
            #print("T2 wins")
            self.guessList.append('T2')

        #sys.exit(0)

if __name__ == '__main__':
    #main()
    obj = LeagueOfLegends()
    obj.readData()
    obj.trainLoLModel()
    obj.classify()
