from .dataBase import dataBase
from .constants import DataSourceTypeEnum
from .constants import DataSourceReturnEnum

from .util import csvDataUtil as cdu
from .util import requestUtil as ru


class dataSim(dataBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = None
        self.lastIndex = None

        self.newCyle = False
        self.end = False

    def loadData(self) -> None:
        """
        Loads the simulated data into self.data
        """
        if self.dataType == DataSourceTypeEnum.CSV:
            keyData = cdu.loadSingleCSV(
                self.key, index=self.indexName, dayFirst=self.dayFirst
            )
            self.key = keyData[0]
            self.data = keyData[1]
        elif self.dataType == DataSourceTypeEnum.DIR:
            keyData = cdu.combineDirCSV(self.key, index="Local time")
            self.key = keyData[0]
            self.data = keyData[1]
        elif self.dataType == DataSourceTypeEnum.URL:
            self.data = ru.getPandasFromUrl(self.key)

        self.data = self.dataModifications(self.data)

    def getData(self) -> dict:
        """
        Called by feeds to get Data, returns the amount of data necessary from the loaded data

        @returns: pandas dataframe of values
        """
        afterData = None
        if self.lastIndex is None:
            self.lastIndex = self.data.index[0]
        elif self.lastIndex == self.data.tail(1).index:
            return None
        else:
            # if just sent a new cycle message then reset new cycle var
            if self.newCycle:
                self.newCycle = False
            elif self.hasConstraints():
                # if constraints are set check to make sure were in current cycle, if not send reset
                # DataSourceReturnEnum.OUTSIDE_CONSTRAINT
                # if eventually do something other than times, this will need to be changed
                if self.lastIndex.day != self.data.loc[self.lastIndex :].index[1].day:
                    self.newCycle = True
                    return DataSourceReturnEnum.OUTSIDE_CONSTRAINT

            # if made it here, set lastIndex to next index
            self.lastIndex = self.data.loc[self.lastIndex :].index[1]

        afterData = self.data.loc[self.lastIndex :]
        timesAfter = afterData.index
        index = -1
        for idx, time in enumerate(timesAfter):
            index = idx
            if (time - self.lastIndex).total_seconds() >= self.period:
                break

        if index == -1:
            # no new values to return
            return None
        elif index == 0:
            return self.data.loc[self.lastIndex :]
        else:
            return afterData[:index]
