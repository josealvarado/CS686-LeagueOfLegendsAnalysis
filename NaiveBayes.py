import ast
import sys
import math
from random import shuffle

def jose():
    print "Jose"

    data = loadJsonFile("datadump.txt")
    training, testing = split_data(data, 600)

    # print "Training Set %d" % len(training)
    # print "Testing Set %d" % len(testing)
    #
    # resultList = []
    # for i in range(0, 100):
    #     shuffle(data)
    #     training, testing = split_data(data, 600)
    #     result = singleFeatureNaiveBayesFirstTower(training, testing, True)
    #     resultList.append(result)
    # print "Average Result %02f" % (sum(resultList) / len(resultList))
    #
    # newData = getQueueType(data, ['NORMAL_5x5_BLIND', 'ARAM_5x5', 'NORMAL_5x5_DRAFT'])
    # print len(newData)
    #
    # resultList = []
    # for i in range(0, 100):
    #     shuffle(newData)
    #     training, testing = split_data(newData, int(len(newData) * .8))
    #     result = singleFeatureNaiveBayesFirstTower(training, testing, False)
    #     resultList.append(result)
    # print "Average Result %02f" % (sum(resultList) / len(resultList))

    firstFeaturesNaiveBayes(training, testing, ['firstTower', 'firstBlood', 'firstBaron', 'firstInhibitor', 'firstDragon', 'assists','deaths','kills'], False)

    # decisionTree(data)

def decisionTree(data):
    print "Decision Tree"
    features = ['firstTower', 'firstBlood']

    results = getWinsandLoasses(data, features)

    # while len(features) > 0:

    informationGainPerFeature = {}
    h = H(results['Wins'], results['Loses'])
    total = results['Wins'] + results['Loses']
    print total

    for feature in features:
        print feature
        valueTrueFalseFeature = results[feature][True][False]
        valueTrueTrueFeature = results[feature][True][True]

        valueTrueFeature = H(valueTrueTrueFeature, valueTrueFalseFeature)
        # print valueTrueFeature

        valueFalseFalseFeature = results[feature][False][False]
        valueFalseTrueFeature = results[feature][False][True]

        valueFalseFeature = H(valueFalseTrueFeature, valueFalseFalseFeature)
        print valueFalseFeature

        impurityPerFeature = 1.0 * (valueTrueFalseFeature + valueTrueTrueFeature) / total * valueTrueFeature + 1.0 * (valueFalseFalseFeature + valueFalseTrueFeature) / total * valueFalseFeature

        informationGainPerFeature[feature] = impurityPerFeature

    print informationGainPerFeature


def H(p, n):
    print p
    print n
    return 1.0* -p/(p+n) * math.log(1.0 * p/(p+n), 2) - 1.0 * n/(p+n) * math.log(1.0 * n/(p+n),2)

def getWinsandLoasses(newData, teamFeatures):
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

    for index, match in enumerate(newData):
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

    # print totalCount
    return totalCount

def getNumberOfBuckets(feature):
    if feature == 'kills':
        return 3
    elif feature == 'deaths':
        return 3
    elif feature == 'assists':
        return 3
    elif feature == 'goldEarned':
        return 3
    elif feature == 'minionsKilled':
        return 3
    elif feature == 'largestKillingSpree':
        return 3
    elif feature == 'largestMultiKill':
        return 3
    elif feature == 'totalDamageTaken':
        return 3
    elif feature == 'totalDamageDealt':
        return 3
    else:
        return 3

def getBucketsForFeature(training, feature):
    print feature
    buckets = []
    numberOfBuckets = getNumberOfBuckets(feature)
    list = []
    for index, match in enumerate(training):
        participants = match['participants']
        for participant in participants:
            kills = participant['stats'][feature]
            list.append(kills)

    list.sort()
    print list
    minValue = min(list)
    maxValue = max(list)
    print "minValue: " + str(minValue) + " maxValue: " + str(maxValue)
    increment = (1.0 * maxValue / numberOfBuckets)
    print increment

    for index in range(numberOfBuckets):
        if index == 0:
            buckets.append((minValue,increment - .000001))
        elif index == numberOfBuckets-1:
            buckets.append((increment * index, maxValue))
        else:
            buckets.append((increment * index, increment + increment * index - .00001))

    print buckets
    return buckets

def getBucketForValue(value, buckets):
    for bucket in buckets:
        min = bucket[0]
        max = bucket[1]
        if min <= value and value <= max:
            return bucket

def getValidListOfContinousFeatures():
    return ['totalDamageTaken','totalDamageDealt','largestMultiKill','largestKillingSpree','minionsKilled','goldEarned','assists','deaths','kills']

def getValidListOfBooleanFeatures():
    return ['firstTower', 'firstBlood', 'firstBaron', 'firstInhibitor', 'firstDragon']

def firstFeaturesNaiveBayes(training, testing, teamFeatures, debug):
    totalCount = {}
    totalCount['Wins'] = 0
    totalCount['Loses'] = 0

    # print test
    for feature in teamFeatures:
        totalCount[feature] = {}
        if feature in getValidListOfContinousFeatures():
            buckets = getBucketsForFeature(training, feature)
            # print feature
            # print buckets
            totalCount[feature]['buckets'] = buckets
            for bucket in buckets:
                totalCount[feature][bucket] = {}
                totalCount[feature][bucket][True] = 0
                totalCount[feature][bucket][False] = 0
        else:
            totalCount[feature][True] = {}
            totalCount[feature][True][True] = 0
            totalCount[feature][True][False] = 0

            totalCount[feature][False] = {}
            totalCount[feature][False][True] = 0
            totalCount[feature][False][False] = 0

    print totalCount

    for index, match in enumerate(training):

        participants = match['participants']
        for participant in participants:
            for feature in teamFeatures:
                if feature in getValidListOfContinousFeatures():
                    kills = participant['stats'][feature]
                    winner = participant['stats']['winner']

                    bucket = getBucketForValue(kills, totalCount[feature]['buckets'])
                    totalCount[feature][bucket][winner] += 1


        teamResults = match['teams']
        for team in teamResults:
            if team['teamId'] == 100:
                if team['winner']:
                    for feature in teamFeatures:
                        if feature in getValidListOfBooleanFeatures():
                            totalCount[feature][team[feature]][True] += 1
                    totalCount['Wins'] += 1
                else:
                    for feature in teamFeatures:
                        if feature in getValidListOfBooleanFeatures():
                            totalCount[feature][team[feature]][False] += 1
                    totalCount['Loses'] += 1
            # Should not ignore the results from team 2

    print totalCount

    # The log-joint distribution over legal labels where True means winner and False means loser
    k = 0.1
    correctPredictions = 0
    for index, match in enumerate(testing):
        totalTrue = 0
        totalFalse = 0

        teamResults = match['teams']
        for team in teamResults:
            if team['teamId'] == 100:

                for feature in teamFeatures:
                    if feature in getValidListOfBooleanFeatures():
                        valueTrue = (totalCount[feature][team[feature]][True] + k) / float(totalCount['Wins'])
                        totalTrue += valueTrue

                        valueFalse = (totalCount[feature][team[feature]][False] + k) / float(totalCount['Loses'])
                        totalFalse += valueFalse
                break


        participants = match['participants']
        for participant in participants:
            for feature in teamFeatures:
                if feature in getValidListOfContinousFeatures():
                    # print participant
                    kills = participant['stats'][feature]

                    bucket = getBucketForValue(kills, totalCount[feature]['buckets'])
                    if bucket == None:
                        print "FATAL ERROR"
                        print feature
                        print kills
                        print totalCount[feature]['buckets']

                    valueTrue = (totalCount[feature][bucket][True] + k) / float(totalCount['Wins'])
                    totalTrue += valueTrue

                    valueFalse = (totalCount[feature][bucket][False] + k) / float(totalCount['Loses'])
                    totalFalse += valueFalse


        probTrue = math.log(1.0 * totalCount['Wins'] / len(training))
        probFalse = math.log(1.0 * totalCount['Loses'] / len(training))

        totalTrue += probTrue
        totalFalse += probFalse

        # print totalTrue
        # print totalFalse

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