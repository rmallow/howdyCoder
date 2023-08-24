from .dataBase import dataBase

import typing
from collections import deque


class dataInput(dataBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data_queue = deque()

    def addData(self, data: typing.Any):
        self._data_queue.append(data)

    def getData(self):
        self.getDataLogging()
        if self._data_queue:
            return self._data_queue.popleft()

    def loadData(self):
        pass
