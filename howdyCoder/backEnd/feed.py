from .dataBase import dataBase

from ..commonUtil.sparseDictList import SparseDictList
from ..commonUtil import mpLogging
from ..core.commonGlobals import DATA_GROUP
from .constants import FeedRetValues

import typing


class feed:
    """
    data storage and processing system for algos
    contains multiple containers for data and calc data along with new/all
    appending functions for pandas data
    """

    def __init__(self, dataSources: list[dataBase]):
        self.dataSources = dataSources
        self.data_source_mapping = {
            data_source.code: data_source for data_source in self.dataSources
        }
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
                    # has to be alist instead of tuple as we could reassign
                    ret_vals.append(
                        [
                            ds_return,
                            data_source.code,
                            data_source.flatten,
                            data_source.output[0],
                        ]
                    )

        self.newCalcLength = 0
        if ret_vals:
            # find the longest
            self.newCalcLength = 1
            for x in range(len(ret_vals)):
                ds_ret, _, flatten, first_output = ret_vals[x]
                try:
                    """
                    data source return values can either be multi column in forms of dict
                    or single column in form of anything else, in which case the first output string is assigned as the
                    key in the dict, there can be no multi column output that doens't come from the ds in dict
                    """
                    ds_ret.values()
                except AttributeError as e:
                    ds_ret = {first_output: ds_ret}
                    ret_vals[x][0] = ds_ret
                if flatten:
                    for v in ds_ret.values():
                        if isinstance(v, list):
                            self.newCalcLength = max(len(v), self.newCalcLength)

            self.data.appendDataList(ret_vals)
        return FeedRetValues.VALID_VALUES if ret_vals else FeedRetValues.NO_VALID_VALUES

    def clear(self) -> None:
        self.data = SparseDictList()
        self.calcData = SparseDictList()

    def getNewCalcLength(self) -> int:
        return self.newCalcLength

    def getDataLength(self) -> int:
        return self.data.getLengthOfLongestList()

    def getNewCombinedDataOfLength(
        self, length: int = None, ignore_last_sent=False
    ) -> SparseDictList:
        def getNewData(data: SparseDictList):
            res = {}
            for k, v in data.items():
                res[k] = (
                    v[::]
                    if ignore_last_sent
                    else v[self.last_sent_data.get(k, 0) : len(v)]
                )
                if length is not None:
                    res[k] = res[k][-length:]
                self.last_sent_data[k] = len(v)
            return res

        ret = SparseDictList()
        ret.appendDictList(getNewData(self.data))
        ret.appendDictList(getNewData(self.calcData))
        return ret

    def getAllData(self):
        ret = SparseDictList()
        ret.appendDictList(self.data)
        ret.appendDictList(self.calcData)
        return ret

    def appendCalcData(self, key: str, index: int, value: typing.Any):
        self.calcData.appendData(key, index, value)

    def started(self):
        for data_source in self.dataSources:
            data_source.just_started = True

    def addInputData(self, data_source_code: str, data: typing.Any):
        if data_source_code in self.data_source_mapping:
            try:
                self.data_source_mapping[data_source_code].addData(data)
            except AttributeError as e:
                mpLogging.error(
                    "Error adding data to data source",
                    description=f"Could not add data to {data_source_code} as it lacks an addData function",
                    group=DATA_GROUP,
                )
        else:
            mpLogging.error(
                "Error adding data to data source",
                description=f"Could not add data to {data_source_code} as it couldn't be found in the feed data source mapping",
                group=DATA_GROUP,
            )
