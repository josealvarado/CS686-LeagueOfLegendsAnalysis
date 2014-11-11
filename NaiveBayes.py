import ast
import sys
import math
from random import shuffle

def jose():
    print "Jose"

    data = loadJsonFile("datadump.txt")
    training, testing = split_data(data, 600)

    print "Training Set %d" % len(training)
    print "Testing Set %d" % len(testing)

    resultList = []
    for i in range(0, 100):
        shuffle(data)
        training, testing = split_data(data, 600)
        result = singleFeatureNaiveBayesFirstTower(training, testing, True)
        resultList.append(result)
    print "Average Result %02f" % (sum(resultList) / len(resultList))

    newData = getQueueType(data, ['NORMAL_5x5_BLIND', 'ARAM_5x5', 'NORMAL_5x5_DRAFT'])
    print len(newData)

    resultList = []
    for i in range(0, 100):
        shuffle(newData)
        training, testing = split_data(newData, int(len(newData) * .8))
        result = singleFeatureNaiveBayesFirstTower(training, testing, False)
        resultList.append(result)
    print "Average Result %02f" % (sum(resultList) / len(resultList))

    firstFeaturesNaiveBayes(training, testing, ['firstTower', 'firstBlood', 'firstBaron', 'firstInhibitor', 'firstDragon'], False)

def firstFeaturesNaiveBayes(training, testing, teamFeatures, debug):
    totalCount = {}
    totalCount['Wins'] = 0
    totalCount['Loses'] = 0
    # Initialize count
    for feature in teamFeatures:
        totalCount[feature] = {}
        totalCount[feature][True] = {}
        totalCount[feature][True][True] = 0
        totalCount[feature][True][False] = 0

        totalCount[feature][False] = {}
        totalCount[feature][False][True] = 0
        totalCount[feature][False][False] = 0

    for index, match in enumerate(training):
        teamResults = match['teams']

        for team in teamResults:
            if team['teamId'] == 100:
                if team['winner']:
                    for feature in teamFeatures:
                        totalCount[feature][team[feature]][True] += 1
                    totalCount['Wins'] += 1
                else:
                    for feature in teamFeatures:
                        totalCount[feature][team[feature]][False] += 1
                    totalCount['Loses'] += 1
            # Should not ignore the results from team 2

    print totalCount

    # The log-joint distribution over legal labels where True means winner and False means loser
    k = 0.1
    correctPredictions = 0
    for index, match in enumerate(testing):
        teamResults = match['teams']
        for team in teamResults:
            if team['teamId'] == 100:
                totalTrue = 0
                totalFalse = 0
                for feature in teamFeatures:
                    valueTrue = (totalCount[feature][team[feature]][True] + k) / float(totalCount['Wins'])
                    totalTrue += valueTrue

                    valueFalse = (totalCount[feature][team[feature]][False] + k) / float(totalCount['Loses'])
                    totalFalse += valueFalse

                probTrue = math.log(1.0 * totalCount['Wins'] / len(training))
                probFalse = math.log(1.0 * totalCount['Loses'] / len(training))

                totalTrue += probTrue
                totalFalse += probFalse

                print totalTrue
                print totalFalse

                winLose = team['winner']

                if totalTrue > totalFalse:
                    if winLose == True:
                        correctPredictions += 1
                else:
                    if winLose == False:
                        correctPredictions += 1

    result = correctPredictions * 1.0 / len(testing) * 100
    print "Correctly Predicted %d out of %d or %.02f%%" % (correctPredictions, len(testing), result)

def singleFeatureNaiveBayesFirstTower(training, testing, debug):
    firsTower = {}
    firsTower[True] = 0
    firsTower[False] = 0

    for index, match in enumerate(training):
        teamResults = match['teams']
        
        for team in teamResults:
            if team['winner'] == True:
                firsTower[team['firstTower']] += 1

    print firsTower

    majorityResult = None

    if firsTower[True] > firsTower[False]:
        majorityResult = True
    else:
        majorityResult = False

    correctClassiciation = 0

    for index, match in enumerate(testing):
        teamResults = match['teams']

        for team in teamResults:
            if team['firstTower'] == majorityResult:
                if team['winner'] == True:
                    correctClassiciation += 1
    if debug:
        print "Naive Bayes Single Feature 'firstTower'"
    result = correctClassiciation * 1.0 / len(testing) * 100
    if debug:
        print "Correctly Predicted %d out of %d or %.02f%%" % (correctClassiciation, len(testing), result)

    return result

def mitchell():
    print "Mitchell"

def keerti():
    print "Keerti"

def getQueueType(data, queueTypes):
    newData = []
    for index, match in enumerate(data):
        if match['queueType'] in queueTypes:
            newData.append(match)
    return  newData

def split_data(data, num):
    training = []
    testing = []

    for index, value in enumerate(data):
        if index < num:
            training.append(value)
        else:
            testing.append(value)

    return training, testing

def loadJsonFile(file):

    jsonData = open(file)
    data = []

    for index, json in enumerate(jsonData):
        # print index
        dictMatch = ast.literal_eval(json)
        data.append(dictMatch)
        # print dictMatch
        # print dictMatch['matchId']

        if index % 100 == 0:
            print "Loading data from file"

    shuffle(data)
    return data

if __name__ == '__main__':
    jose()
    mitchell()
    keerti()
