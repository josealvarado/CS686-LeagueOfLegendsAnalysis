__author__ = 'josealvarado'

import ast
import math
from random import shuffle

class DecisionTree():
    '''
    Sklearn-style decision tree classifier, using entropy
    '''
    def __init__(self, file_name = "datadump.txt", features = ['firstTower', 'firstBlood', 'firstBaron', 'firstInhibitor'], attrib_d=None, attribs=None, default_v=None):
        ''' initialize classifier
        '''

        self.data = self.loadJsonFile(file_name)
        print len(self.data)

        self.features = features

        # if not attribs:
        #     attribs = []
        # if attrib_d:
        #     self.attrib_dict = attrib_d
        # else:
        #     self.attrib_dict = {}
        # self.attribute_list = attribs
        # self.default_value = default_v

        "*** YOUR CODE HERE AS NEEDED ***"

    def loadJsonFile(self, file_name):
        jsonData = open(file_name)
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

    def getResults(self, data, features):
        totalCount = {}
        totalCount['Wins'] = 0
        totalCount['Loses'] = 0
        # Initialize count
        for feature in features:
            totalCount[feature] = {}
            totalCount[feature][True] = {}
            totalCount[feature][True][True] = 0
            totalCount[feature][True][False] = 0

            totalCount[feature][False] = {}
            totalCount[feature][False][True] = 0
            totalCount[feature][False][False] = 0

        for index, match in enumerate(data):
            teamResults = match['teams']

            for team in teamResults:
                if team['teamId'] == 100:
                    if team['winner']:
                        for feature in features:
                            totalCount[feature][team[feature]][True] += 1
                        totalCount['Wins'] += 1
                    else:
                        for feature in features:
                            totalCount[feature][team[feature]][False] += 1
                        totalCount['Loses'] += 1
                # Should not ignore the results from team 2

        return totalCount

    def fit(self, data=1, features=1):
        '''X and y are as in sklearn classifier.fit expected arguments
        Creates a decision tree
        '''
        "*** YOUR CODE HERE AS NEEDED***"
        # self.clf = self.makeTree(X, y, self.attribute_list, self.attrib_dict, self.default_value)

        self.results = self.getResults(self.data, self.features)
        print self.results

        self.tree = self.makeTree(self.data, self.features, self.features[0])
        # print self.tree
        self.printTree(self.tree)

    def printTree(self, root, val='Tree', indentNum=0):
        """
        For printing the decision tree in a nice format
        """
        # print root
        indent = "\t"*indentNum
        if root.is_leaf():
            print indent+"+-"+str(val)+'-- '+str(root.value)

        else:
            print indent+"+-"+str(val)+'-- <'+root.feature+'>'
            print indent+"{"
            for k in root.children.keys():
                self.printTree(root.children[k],k,indentNum+1)
            print indent+"}"

    def predict(self, X):
        ''' Return a class label using the decision tree created by the fit method
        '''
        "*** YOUR CODE HERE AS NEEDED***"
        #call recursive classify method on the learned tree for each x in X



    def entropy(self, valTrue, valFalse):
        """
        Calculates the entropy of the given data set for the target attribute
        """
        if valTrue == 0 or valFalse == 0:
            return 0

        data_entropy = 0.0
        for val in [valTrue, valFalse]:
            data_entropy += (-1.0 * val)/(valTrue + valFalse) * math.log(1.0 * val / (valTrue + valFalse), 2)

        # print "data_entropy" + str(data_entropy)
        return data_entropy

    # ### Compute remainder - this is the amount of entropy left in the data after
    # ### we split on a particular attribute. Let's assume the input data is of
    # ### the form:
    # ###    [(value1, class1), (value2, class2), ..., (valuen, classn)]
    # def remainder(self, data) :
    #     possibleValues = set([item[0] for item in data])
    #     r = 0.0
    #     for value in possibleValues :
    #         c = [item[0] for item in data].count(value)
    #         r += (float(c) / len(data) ) * self.entropy([item[1] for item in
    #                                             data if item[0] == value])
    #     return r


    def informationGain(self, data, entropyOfWholeData, feature, results):
        """
        Calculates the information gain (reduction in entropy) that would
        result by splitting the data on the chosen feature
        """
        subset_entropy = 0.0
        subset = results[feature]
        # print subset

        # Calculate the sum of the entropy for each subset of records weighted
        # by their probability of occurring in the training set.
        for val in subset.keys():
            valTrue = results[feature][val][True]
            valFalse = results[feature][val][False]
            val_prob = 1.0 * (valTrue + valFalse) / len(data)

            # print "valTrue: " + str(valTrue)
            # print "valFalse: " + str(valFalse)
            # print "val_prob: " + str(val_prob)
            subset_entropy += val_prob * self.entropy(valTrue, valFalse)

        # print "subset_entropy" + str(subset_entropy)
        # print "information_gain" + str(entropyOfWholeData- subset_entropy)

        # Subtract the entropy of the chosen attribute from the entropy of the
        # whole data set with respect to the target attribute (and return it)
        return (entropyOfWholeData- subset_entropy)

    def selectFeature(self, data, features):
        print "selectFeature"
        """
        Selects the feature to best classify our data
        Represented by the lowest information gain
        """
        informationGainPerFeature = {}

        for feature in features:
            # print feature
            results = self.getResults(data, features)

            entropyOfWholeData = self.entropy(results["Wins"], results["Loses"])
            # print "wins: " + str(self.results["Wins"]) + " loss: " + str(self.results["Loses"])
            # print "entropyOfWholeData: " + str(entropyOfWholeData)
            informationGainPerFeature[feature] = self.informationGain(data, entropyOfWholeData, feature, results)
        print informationGainPerFeature

        if len(informationGainPerFeature) > 0:
            return min(informationGainPerFeature, key=informationGainPerFeature.get)
        else:
            return None

    def get_examples(self, data, feature, feature_value):
        print "get_examples"
        new_data = []
        for index, match in enumerate(data):
            teamResults = match['teams']

            for team in teamResults:
                if team['teamId'] == 100:
                    if team[feature] == feature_value:
                        new_data.append(match)
        return new_data

    def get_values(self, data, feature):
        print "get_values"
        new_data = []
        for index, match in enumerate(data):
            teamResults = match['teams']

            for team in teamResults:
                if team['teamId'] == 100:
                    new_data.append(team['winner'])
                    # print team[feature]
        return new_data

        # results = self.getResults(data, [best_feature])
        # subset = results[best_feature]

    def get_majority_value(self, data, feature):
        print "get_majority_value"
        results = self.getResults(data, [feature])
        wins = results["Wins"]
        loss = results["Loses"]
        if wins >= loss:
            return True
        else:
            return False

    def get_feature_values(self, feature):
        if feature == "firstTower":
            return [True, False]
        elif feature == 'firstBlood':
            return [True, False]
        return None

    ### a tree is simply a data structure composed of nodes (of type TreeNode).
    ### The root of the tree
    ### is itself a node, so we don't need a separate 'Tree' class. We
    ### just need a function that takes in a dataset and our attribute dictionary,
    ### builds a tree, and returns the root node.
    ### makeTree is a recursive function. Our base case is that our
    ### dataset has entropy 0 - no further tests have to be made. There
    ### are two other degenerate base cases: when there is no more data to
    ### use, and when we have no data for a particular value. In this case
    ### we use either default value or majority value.
    ### The recursive step is to select the attribute that most increases
    ### the gain and split on that.
    ### assume: input looks like this:
    ### dataset: [[v11, v21, ..., vd1], [v12,v22, ..., vd2] ...[v1n,v2n,...vdn] ],
    ###    remaining training examples with values for only the unused features
    ### labels: [c1, ..., cn], remaining target labels for the dataset
    ### attributes: [a1, a2, ...,ax] the list of remaining attribute names
    ### attrib_dict: {a1: [a1vals], a2: [a2vals],...,ad: [advals]}
    ### the dictionary keys are attribute names and the dictionary values are either the list
    ### of values that attribute takes on or 'real' for real-valued attributes (handle for Extra Credit)
    # def makeTree(self, dataset=1, labels=1, attributes=1, attrib_dict=1, defaultValue=1):
    def makeTree(self, data, features, target_feature=1, defaultValue=1):
        ''' Helper recursive function for creating a tree
        '''

        print "Data Size: " + str(len(data)) + ", Features: " + str(features) + ", Target_Feature: " + target_feature
        # print data
        vals = self.get_values(data, target_feature)
        print vals
        default = self.get_majority_value(data, target_feature)

        # If the dataset is empty or the attributes list is empty, return the
        # default value. When checking the attributes list for emptiness, we
        # need to subtract 1 to account for the target attribute.
        if len(data) <= 0 or len(features) <= 0:
            print "Case 1"
            subset = TreeNode()
            subset.value = default
            return subset

        # If all the records in the dataset have the same classification, return that classification.
        elif vals.count(vals[0]) == len(vals):
            print "Case 2"
            print vals.count(vals[0])
            print len(vals)
            subset = TreeNode()
            subset.value = vals[0]
            return subset

        else:
            # Choose the next best attribute to best classify our data
            best_feature = self.selectFeature(data, features)
            print best_feature

            # Create a new decision tree/node with the best feature
            tree_node = TreeNode(best_feature)
            # tree_node.feature = best_feature

            # Create a new decision tree/sub-node for each of the values
            # in the best feature
            results = self.getResults(data, [best_feature])
            subset = results[best_feature]
            print subset
            for val in subset.keys():

                # Create a subtree for the current value under the "best" field
                subTree = self.makeTree(self.get_examples(data, best_feature, val), [feature for feature in features if feature != best_feature], best_feature)
                # subTree = TreeNode(value = val)
                tree_node.children[val] = subTree

        return tree_node

### Helper class for DecisionTree.
### A TreeNode is an object that has either:
### 1. A feature to be tested and a set of children, one for each possible
### value of the feature, OR
### 2. A value (if it is a leaf in a tree)
class TreeNode:
    def __init__(self, feature = 0, value = 0):
        self.feature = feature
        self.value = value
        self.children = {}

    # def __repr__(self):
    #     if self.feature:
    #         return self.feature
    #     else:
    #         return self.value

    ### a node with no children is a leaf
    def is_leaf(self):
        return self.children == {}

    ###
    def classify(self, x, attributes, default_value):
       '''
       return the value for the given data
       the input will be:
       x - an object to classify - [v1, v2, ..., vn]
        attributes - the names of all the attributes
       '''
       "*** YOUR CODE HERE ***"




if __name__ == '__main__':
    tree = DecisionTree()
    tree.fit()
