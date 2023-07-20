import json
import re, sys
import os
import pandas as pd
from math import *
from yaml import *
import urllib.request


def getJsonDataStr(url):
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")


def testMessageFunc(dataSet):
    return "testMessage"


def testFunc(dataSet):
    return dataSet["close"].iloc[0] + 1


def testManip(dataSet):
    return dataSet.iloc[0][0] + 1


def ema(dataSet, smooth=2):
    period = len(dataSet.index)
    ema = None
    for _, row in dataSet.iterrows():
        if ema is None:
            ema = row[0]
        else:
            ema = row[0] * (smooth / (period + 1)) + ema * (1 - (smooth / (period + 1)))
    return ema


def testFunc(dataSet):
    """
    algoBuilder

    some other super long description
    """
    pass


def sma(dataSet):
    """algoBuilder"""
    return dataSet.iloc[:, 0].mean()


def change(dataSet):
    """algoBuilder"""
    try:
        return dataSet.iloc[-1][0] - dataSet.iloc[0][0]
    except IndexError:
        return 0


def up(dataSet):
    """algoBuilder"""
    if dataSet.iloc[0][0] > 0:
        return dataSet.iloc[0][0]
    else:
        return 0


def down(dataSet):
    """algoBuilder"""
    if dataSet.iloc[-1][0] < 0:
        return dataSet.iloc[-1][0] * -1
    else:
        return 0


def divide(dataSet):
    """algoBuilder"""
    if dataSet.iloc[0][1] == 0:
        return 0
    else:
        return dataSet.iloc[0][0] / dataSet.iloc[0][1]


def multiply(dataSet):
    """algoBuilder"""
    return dataSet.iloc[0][0] * dataSet.iloc[0][1]


def multiplyFactor(dataSet, factor=2):
    """algoBuilder"""
    return dataSet.iloc[0][0] * factor


def rsi(dataSet, parameters=None):
    """algoBuilder"""
    return 100 - (100 / (1 + dataSet.iloc[0][0]))


def cryptoCount(dataSet, cryptoSet=None):
    """algoBuilder"""
    if cryptoSet is None:
        cryptoSet = set()
    words = dataSet.iloc[0][0]
    wordsSplit = words.split(" ")
    count = 0
    for word in wordsSplit:
        if word.lower() in cryptoSet:
            count += 1
    return count


def wordCount(dataSet):
    """algoBuilder"""
    words = dataSet.iloc[0][0]
    wordsSplit = words.split(" ")
    return len(wordsSplit)


def searchTermCount(dataSet, word=""):
    """algoBuilder"""
    words = dataSet.iloc[0][0].lower()
    count = sum(1 for _ in re.finditer(r"\b%s\b" % re.escape(word), words))
    return count


def loadCryptoNames(url=None, **kwargs):
    """algoBuilder"""
    cryptoSet = set()
    if url:
        jsonStr = getJsonDataStr(url)
        jList = json.loads(jsonStr)
        for item in jList:
            cryptoSet.add(item["symbol"].removesuffix("USD").lower())
    return cryptoSet


def loadCryptoNamesList(url=None, **kwargs):
    """algoBuilder"""
    cryptoSet = []
    if url:
        jsonStr = getJsonDataStr(url)
        jList = json.loads(jsonStr)
        for item in jList:
            cryptoSet.append(item["symbol"].removesuffix("USD").lower())
    return cryptoSet


# Testing function for duplicating a column
def duplicate(dataSet):
    if len(dataSet.iloc[0].values) > 1:
        return "More than 1 value"
    return dataSet.iloc[0][0]


def sumRow(dataSet):
    return dataSet.iloc[0].sum()


def testNoArgEvent():
    return 0


def renameTest(dataSet, word):
    return word
