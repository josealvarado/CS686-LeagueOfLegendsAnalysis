_author_ = "Keerti Sekhar Sahoo"
import json
import sys
import ast
from sklearn.cross_validation import KFold
# This implementation is for checking a single features influence in a match
def NaiveBayesLoL():
    print"LoL"
    data_file = "datadump.txt"
    txt = open(data_file)
    feature = 'towerKills'
    data = []
    queueType = 'NORMAL_5x5_BLIND'
    #queueType = 'ARAM_5x5'
    #queueType = "ALL"
    for i,dat in enumerate(txt):
        dat = ast.literal_eval(dat)
        if dat['queueType'] == queueType:
            dat = str(dat)
            data.append(dat)
        elif queueType == 'ALL':
            dat = str(dat)
            data.append(dat)
    #print("data",data[5])
    #sys.exit(0)
    trainSet = []
    testSet = []
    kf = KFold(len(data),n_folds = 10)
    for train,test in kf:
        for index in train:
            trainSet.append(data[index])
        for index in test:
            testSet.append(data[index])
        break
    ''' Train the model '''
    print("Training.......")
    trueWin =0.0
    falseWin = 0.0
    for i, match in enumerate(trainSet):
        dict = ast.literal_eval(match) #single match data. type dict

        teamsInfo = dict['teams'] # info about two teams in a match. type dict
        if teamsInfo[0][feature] > teamsInfo[1][feature] and teamsInfo[0]['winner'] == True or \
            teamsInfo[0][feature] < teamsInfo[1][feature] and teamsInfo[1]['winner'] == True:
            trueWin +=1
        else:
            falseWin +=1
    print("no of true wins",trueWin)
    print("no of false wins",falseWin)
    percnt = (trueWin/len(trainSet)) * 100
    #print("percent",percnt)
    # if trueWin > falseWin:
    #     print"Team with max feature wins ",percent,"percent " + " of times"
    ''' Testing'''
    print("Testing.......")
    guesses = []
    results = []
    for i,match in enumerate(testSet):
        dict = ast.literal_eval(match)
        teamsInfo = dict['teams']
        if teamsInfo[0][feature] > teamsInfo[1][feature]:
            guesses.append(True)
            results.append(teamsInfo[0]['winner'])
        elif teamsInfo[0][feature] < teamsInfo[1][feature]:
            guesses.append(True)
            results.append(teamsInfo[1]['winner'])
    count = 0.0
    for i in range(0,len(guesses)):
        if guesses[i] == results[i]:
            count +=1
    accuracy = (count/len(guesses)) * 100
    #print(accuracy)
    print "Probability of the team wining with max number of feature is:",accuracy,"percent"
    sys.exit(0)



def main():
    NaiveBayesLoL()

if __name__ == '__main__':
    main()