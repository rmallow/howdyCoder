from .dataBase import DataBase

from .util import requestUtil as ru

import time


class dataStream(DataBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _getData(self) -> dict:
        return self.dataModifications(self.getDataReal())

    def getDataReal(self):
        return ru.getUrlData(self.key)

    def loadData(self):
        return
