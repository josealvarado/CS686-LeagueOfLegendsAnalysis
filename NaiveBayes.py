import ast
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
        result = singleFeatureNaiveBayesFirstTower(training, testing)
        resultList.append(result)
    print "Average Result %02f" % (sum(resultList) / len(resultList))

def singleFeatureNaiveBayesFirstTower(training, testing):
    firsTower = {}
    firsTower[True] = 0
    firsTower[False] = 0

    for index, match in enumerate(training):
        teamResults = match['teams']
        
        for team in teamResults:
            if team['winner'] == True:
                firsTower[team['firstTower']] += 1

    # print firsTower

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

    print "Naive Bayes Single Feature 'firstTower'"
    result = correctClassiciation * 1.0 / len(testing) * 100
    print "Correctly Predicted %d out of %d or %.02f%%" % (correctClassiciation, len(testing), result)

    return result

def mitchell():
    print "Mitchell"

def keerti():
    print "Keerti"

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
