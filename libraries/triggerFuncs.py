import numpy as np


def testFunc(dataSet, parameters=None):
    """algoBuilder"""
    return "testMessage"


def crossover(dataSet, parameters):
    """algoBuilder"""
    before = np.sign(dataSet.iloc[0, 0] - dataSet.iloc[0, 1])
    after = np.sign(dataSet.iloc[1, 0] - dataSet.iloc[1, 1])
    if before != after:
        return dataSet.index[0]
    else:
        return None


def under(dataSet, parameters=None):
    """algoBuilder"""
    return dataSet.iloc[0, 0] < parameters["factor"]


def over(dataSet, parameters=None):
    """algoBuilder"""
    return dataSet.iloc[0, 0] > parameters["factor"]


def pctDifference(dataSet, parameters=None):
    delta = dataSet.iloc[0, 0] - dataSet.iloc[0, 1]


def sendValue(dataSet, parameters=None):
    """algoBuilder"""
    return dataSet.iloc[0, 0]


def printTest(dataSet):
    print("happy")
    print(dataSet[0][0])
