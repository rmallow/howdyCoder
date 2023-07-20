from ..commonUtil import mpLogging
from ..core.commonGlobals import HANDLER_GROUP

from collections import OrderedDict
from typing import NamedTuple

"""
Stores messages with by keys for handlers to acess quickly

code1:
{
    time1: (0, [data])
    time2: (1, [data])
    time3: (2, [data])
}
code2:
{
    time1: (0, [data])
    time2: (1, [data])
}

"""


class timeData(NamedTuple):
    index: int
    data: list


class handlerData:
    def __init__(self):
        self.dataSet = {}

    """
    @brief: internal method to insert into handler data

    @param: message - must be of message data type!
    """

    def _insert(self, message):
        if message is not None and message.keyExists():
            key = message.key
            if key.sourceCode not in self.dataSet:
                self.dataSet[key.sourceCode] = OrderedDict()

            if key.time not in self.dataSet[key.sourceCode]:
                """
                Why are we storing the index? Because OrderedDict keeps track of the order but not the index
                We need the index in the get method when used with period
                """
                self.dataSet[key.sourceCode][key.time] = timeData(
                    len(self.dataSet[key.sourceCode]), []
                )

            self.dataSet[key.sourceCode][key.time].data.append(message)

    """
    insert one message or list of messages
    """

    def insert(self, rawMessage):
        try:
            for msg in rawMessage:
                self._insert(msg)
        except TypeError:
            self._insert(rawMessage)

    def _getCodeDict(self, key):
        try:
            return self.dataSet[key.sourceCode]
        except Exception:
            mpLogging.warning(
                "Invalid code for handler data access",
                description="Key: " + str(key),
                title=HANDLER_GROUP,
            )
            return None

    def _getTimeData(self, key):
        codeDict = self._getCodeDict(key)

        if codeDict is None:
            return None

        try:
            # the first element is the index of the time, so return the data at second element
            return codeDict[key.time]
        except Exception:
            mpLogging.warning(
                "Invalid code for handler data access",
                description="Key: " + str(key),
                title=HANDLER_GROUP,
            )
            return None

    def get(self, key, default=None):
        timeData = self._getTimeData(key)
        if timeData is not None:
            return timeData.data
        else:
            return default

    def getNames(self, key, default=None):
        # TODO
        pass

    def getPeriod(self, key, period):
        """
        @brief: getter method for getting a period based on key

        @param: key - messageKey data type
        @param: period - int, period to get by

        @return -   handler data return value, get's code dict by key
                    then returns times without index
            time1: [data1]
            time2: [data2]
            ...
            time n : [data n]
            where n is period
        """
        codeDict = self._getCodeDict(key)
        timeData = self._getTimeData(key)

        if timeData is None:
            return None

        timeEndIndex = timeData.index
        timeStartIndex = 0
        if timeEndIndex < period or len(codeDict) < period:
            timeStartIndex = 0
        else:
            timeStartIndex = timeEndIndex - period

        if timeStartIndex != timeEndIndex and period != 1:
            keys = list(codeDict.keys())[timeStartIndex:timeEndIndex]
        else:
            keys = [list(codeDict.keys())[timeEndIndex]]

        # generate new dict and return using these keys, leaving out index
        returnDict = {}
        for k in keys:
            if k in codeDict:
                returnDict[k] = codeDict[k][1]

        return returnDict

    def getPeriodNames(self, key, period):
        pass

    def clearCode(self, code):
        self.dataSet.pop(code, None)
