from .dataBase import dataBase

from ..commonUtil.sparseDictList import SparseDictList
from .constants import FeedRetValues

import collections
import typing


def safeLength(value):
    """
    use this for values that could be an unknown type
    """
    if isinstance(value, collections.Iterable) and not isinstance(value, str):
        return len(value)
    else:
        return 1


class feed:
    """
    data storage and processing system for block
    contains multiple containers for data and calc data along with new/all
    appending functions for pandas data
    """

    def __init__(self, dataSources: list[dataBase]):
        self.dataSources = dataSources
        # feed doesn't have its own period but will instead go every time the fastest ds needs to be refreshed
        self.period = min(ds.period for ds in self.dataSources)

        """
        Data holders for feed:
            data - holds all data in current cycle
            calcData - holds all calculated data in current cycle
        """

        self.data: SparseDictList = SparseDictList()
        self.calcData: SparseDictList = SparseDictList()

        self.last_sent_data = {}

        self.newCalcLength = 0
        self.end = False

    def update(self) -> FeedRetValues:
        """
        Gather up all of the data source return values
        Determine the longest, based on flattening or not, if no data source have flatten the longest is 1
        Append the ret vals from the data sources to data
        """
        ret_vals = []
        for data_source in self.dataSources:
            if data_source.readyToGet():
                # DS get Data should return a dict, so this is a safe check
                if ds_return := data_source.getData():
                    # we need to append to an intermediary for indexing
                    ret_vals.append((ds_return, data_source.code, data_source.flatten))

        self.newCalcLength = 0
        if ret_vals:
            # find the longest
            self.newCalcLength = max(
                len(v) if (isinstance(v, list) and inner[2]) else 1
                for inner in ret_vals
                for v in inner[0].values()
            )
            self.data.appendDataList(ret_vals)
        return FeedRetValues.VALID_VALUES if ret_vals else FeedRetValues.NO_VALID_VALUES

    def clear(self) -> None:
        self.data = SparseDictList()
        self.calcData = SparseDictList()

    def getNewCalcLength(self) -> int:
        return self.newCalcLength

    def getDataLength(self) -> int:
        return self.data.getLengthOfLongestList()

    def getNewCombinedDataOfLength(self, length: int = None) -> SparseDictList:
        def getNewData(data: SparseDictList):
            res = {}
            for k, v in data.items():
                res[k] = v[self.last_sent_data.get(k, 0) : len(v)]
                if length is not None:
                    res[k] = res[k][-length:]
                self.last_sent_data[k] = len(v)
            return res

        ret = SparseDictList()
        ret.appendDictList(getNewData(self.data))
        ret.appendDictList(getNewData(self.calcData))
        return ret

    def appendCalcData(self, key: str, index: int, value: typing.Any):
        self.calcData.appendData(key, index, value)
