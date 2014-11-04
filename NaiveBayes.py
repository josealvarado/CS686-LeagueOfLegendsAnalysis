
import json
import ast

def jose():
    print "Jose"

def mitchell():
    print "Mitchell"

def keerti():
    print "Keerti"

def loadJsonFile(file):

    data = open(file)
    # print data
    # json_data = json.loads(data)
    # print json_data

    for index, value in enumerate(data):
        print index

        value2 = ast.literal_eval(value)
        # print value2
        print value2['matchId']

if __name__ == '__main__':
    jose()
    mitchell()
    keerti()

    loadJsonFile("datadump.txt")

