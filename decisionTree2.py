from sklearn.externals import joblib
import mlUtil
import math
import argparse

#helper method & sample solution for ZeroR fit method
def zeroR(data):
    '''
       Given a list or sklearn-style dictionary, return the most common value
    '''
    if type(data) == dict:
        y_vals = data['target']
    else:
        y_vals = data
    class_counts = dict.fromkeys(y_vals, 0)
    for i in y_vals:
        class_counts[i] += 1
    return max(class_counts, key=class_counts.get)


class DecisionTree():
    '''
    Sklearn-style decision tree classifier, using entropy
    '''
    def __init__(self, attrib_d=None, attribs=None, default_v=None):
        ''' initialize classifier
        '''
        if not attribs:
            attribs = []
        if attrib_d:
            self.attrib_dict = attrib_d
        else:
            self.attrib_dict = {}
        self.attribute_list = attribs
        self.default_value = default_v
        
        "*** YOUR CODE HERE AS NEEDED ***"
        mlUtil.raiseNotDefined()

    def fit(self, X, y):
        '''X and y are as in sklearn classifier.fit expected arguments
        Creates a decision tree
        '''
        "*** YOUR CODE HERE AS NEEDED***"
        self.clf = self.makeTree(X, y, self.attribute_list, self.attrib_dict, self.default_value)
        mlUtil.raiseNotDefined()

    def predict(self, X):
        ''' Return a class label using the decision tree created by the fit method
        '''
        "*** YOUR CODE HERE AS NEEDED***"
        #call recursive classify method on the learned tree for each x in X
        mlUtil.raiseNotDefined()

    def entropy(self, labels):
        '''takes as input a list of class labels. Returns a float
        indicating the entropy in this data.
        Hint: you don't have to implement log_2(x), see math.log()
        '''
        "*** YOUR CODE HERE ***"
        return 0



    ### Compute remainder - this is the amount of entropy left in the data after
    ### we split on a particular attribute. Let's assume the input data is of
    ### the form:
    ###    [(value1, class1), (value2, class2), ..., (valuen, classn)]
    def remainder(self, data) :
        possibleValues = set([item[0] for item in data])
        r = 0.0
        for value in possibleValues :
            c = [item[0] for item in data].count(value)
            r += (float(c) / len(data) ) * self.entropy([item[1] for item in
                                                data if item[0] == value])
        return r

    ###
    def selectAttribute(self, X, y):
        '''
        selectAttribute: choose the index of the attribute in the current
        dataset that minimizes remainder(A).
        '''
        "*** YOUR CODE HERE ***"
        return -1

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
    def makeTree(self, dataset, labels, attributes, attrib_dict, defaultValue):
        ''' Helper recursive function for creating a tree
        '''
        "*** YOUR CODE HERE ***"
        mlUtil.raiseNotDefined()


### Helper class for DecisionTree.
### A TreeNode is an object that has either:
### 1. An attribute to be tested and a set of children, one for each possible
### value of the attribute, OR
### 2. A value (if it is a leaf in a tree)
class TreeNode:
    def __init__(self, attribute, value):
        self.attribute = attribute
        self.value = value
        self.children = {}

    def __repr__(self):
        if self.attribute:
            return self.attribute
        else:
            return self.value

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
       mlUtil.raiseNotDefined()


#here's a way to visually check your tree
def printTree(root, val='Tree', indentNum=0):
    """ For printing the decision tree in a nice format
        Usage: printTree(rootNode)
    """
    indent = "\t"*indentNum
    if root.is_leaf():
        print indent+"+-"+val+'-- '+root.value

    else:
        print indent+"+-"+val+'-- <'+root.attribute+'>'
        print indent+"{"
        for k in root.children.keys():
            printTree(root.children[k],k,indentNum+1)
        print indent+"}"



if __name__ == '__main__':
    #parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("train_file", help="Name of file with training data", type=str)
    parser.add_argument("--y_col", help="name of column containing target", type=str)
    parser.add_argument("--ibm", help="Flag to indicate that input is IBM data, else plain CSV", action="store_true")
    args = parser.parse_args()

    #for you to add is logic for handling the --y_col flag if given (for tennis, for example)
    if args.ibm:
        data = joblib.load(args.train_file)
    else:
        data = mlUtil.extract_data(args.train_file)
    data = mlUtil.enhance_data(data)

    #will need some args in constructor
    tree = DecisionTree('***YOU ADD ARGUMENTS HERE***')
    tree.fit(data['data'], data['target'])
    #pritnTree(tree.clf)
    #test on training data
    tree.predict(data['data'])

