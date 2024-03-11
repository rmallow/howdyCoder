from .dataBase import DataBase

import typing
from collections import deque


class DataExternal(DataBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data_queue = deque()

    def addData(self, data: typing.Any):
        self._data_queue.append(data)

    def _getData(self):
        ret_val = None
        if self._data_queue:
            self.getDataLogging()
            ret_val = self._data_queue.popleft()
        return ret_val

    def loadData(self):
        pass
