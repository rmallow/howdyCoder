from .dataBase import dataBase

from .util import requestUtil as ru

import time


class dataStream(dataBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def getData(self) -> dict:
        return self.dataModifications(self.getDataReal())

    def getDataReal(self):
        return ru.getUrlData(self.key)

    def loadData(self):
        return
