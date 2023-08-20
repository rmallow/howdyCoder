import os
import pandas as pd
import numpy as np
from pathlib import Path


# specify a specific extension to filter for
def getFilesFromDir(path, ext=None):
    (_, _, filenames) = next(os.walk(path))
    filenames.sort()
    if ext is not None:
        filenames = filter(lambda item: (item.endswith(ext)), filenames)

    return filenames


def loadCSV(fullPath, names=None, index='Date', dayFirst=False):
    data = None
    if names is not None:
        data = pd.read_csv(fullPath, header=0, names=names, parse_dates=True,
                           na_filter=True, index_col=index, dayfirst=dayFirst).dropna()
    else:
        data = pd.read_csv(fullPath, header=0, parse_dates=True,
                           na_filter=True, index_col=index, dayfirst=dayFirst).dropna()
    return data


# old version, each CSV loaded as separate dataframe, no appending
def getPandasDataFromCSV(path, names=None, index='Date'):
    output = []
    for file in getFilesFromDir(path, "csv"):
        data = loadCSV(path + "/" + file, names, index)
        key = os.path.splitext(file)[0]
        output.append((key, data))
    return output


def getPctChangeOfCol(dataframe, col):
    arr = dataframe.loc[:, col].to_numpy()
    dates = dataframe.index
    pct = []
    date = []
    for i in range(1, arr.size):
        pct.append([((arr[i] - arr[i-1])/arr[i-1]*100)])
        date.append(dates[i])
    return np.column_stack((date, pct))


# assigns key as last, combines all dataframes to one
def combineDirCSV(path, names=None, index='Date'):
    data = None
    for file in getFilesFromDir(path, "csv"):
        curData = loadCSV(path + "/" + file, names, index)
        if data is None:
            data = curData
        else:
            data.append(curData)
        key = os.path.splitext(file)[0]
    return (key, data)


# only loads one CSV file as key
def loadSingleCSV(path, names=None, index='Date', dayFirst=False):
    fullPath = Path.cwd() / path
    data = loadCSV(fullPath, names, index, dayFirst)
    key = os.path.splitext(os.path.split(path)[1])[0]
    return (key, data)
