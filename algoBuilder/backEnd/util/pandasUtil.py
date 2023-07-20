from ...commonUtil import mpLogging
"""
Functions used for pandas dataFrame modifications
"""


def setIndex(dataFrame, indexName):
    colList = dataFrame.columns
    # set desired column as index
    if indexName and indexName in colList:
        return dataFrame.set_index(indexName)
    else:
        mpLogging.warning("Tried to set index that isn't in the dataframe",
                          description=f"index that was attempted to be set: {indexName}")
    return dataFrame


def filterColumns(dataFrame, columnFilter=None, removeColumns=None):
    colList = dataFrame.columns
    bFiltered = False
    # if filter column is not none, remove all columns that aren't in filter columns
    if columnFilter:
        dropColList = []
        for col in colList:
            if col not in columnFilter:
                dropColList.append(col)

        # not going to drop all columns so make sure they're not the same length
        if len(dropColList) > 0 and len(dropColList) != len(colList):
            bFiltered = True
            dataFrame = dataFrame.drop(dropColList, axis=1)

    # remove columns from removeColumns if we didn't already filter
    if not bFiltered and removeColumns:
        dropColList = []
        for col in removeColumns:
            if col in colList:
                dropColList.append(col)

        if len(dropColList) > 0:
            dataFrame = dataFrame.drop(dropColList, axis=1)

    return dataFrame
