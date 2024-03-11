from .dataBase import DataBase

from ..commonUtil.sparseDictList import SparseDictList
from ..commonUtil import mpLogging
from ..core.commonGlobals import DATA_GROUP
from ..core.dataStructs import Modes
from .constants import FeedRetValues

# from viztracer import log_sparse

import typing


class feed:
    """
    data storage and processing system for algos
    contains multiple containers for data and calc data along with new/all
    appending functions for pandas data
    """

    def __init__(self, dataSources: list[DataBase]):
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

    # @log_sparse
    def update(self) -> FeedRetValues:
        """
        Gather up all of the data source return values
        Determine the longest, based on flattening or not, if no data source have flatten the longest is 1
        Append the ret vals from the data sources to data
        """
        ret_vals = []
        for data_source in self.dataSources:
            ds_return = data_source.getData()
            if ds_return is not None:
                # we need to append to an intermediary for indexing
                # has to be alist instead of tuple as we could reassign
                ret_vals.append(
                    [
                        ds_return,
                        data_source.code,
                        data_source.flatten,
                        not data_source.data_in_rows,
                        data_source.output,
                    ]
                )

        self.newCalcLength = 0
        if ret_vals:
            self.newCalcLength = self.data.appendDataList(ret_vals)
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
            data_source.changeMode(Modes.RUNNING)

    def addSourceData(self, data_source_code: str, data: typing.Any):
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
