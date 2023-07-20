import pandas
from urllib.request import urlopen
import json


def getJsonDataStr(url):
    response = urlopen(url)
    return response.read().decode("utf-8")


def getPandasFromUrl(url):
    jsonStr = getJsonDataStr(url)
    return pandas.read_json(path_or_buf=jsonStr)


def getUrlData(url):
    jsonStr = getJsonDataStr(url)
    data = json.loads(jsonStr)
    return data
