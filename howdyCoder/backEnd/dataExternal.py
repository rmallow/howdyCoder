from .dataBase import DataBase
from ..core.dataStructs import Modes

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
            ret_val = self._data_queue.popleft()
            if ret_val is None and not self._data_queue:
                # if None is on the data queue and there's nothing left on the queue this is an indication of finished
                self.changeMode(Modes.FINISHED)
            else:
                self.getDataLogging()
        return ret_val

    def loadData(self):
        pass
