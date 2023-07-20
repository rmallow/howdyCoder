from .constants import DataSourceTypeEnum, DataSourceReturnEnum

from ..commonUtil import mpLogging
from ..core.commonGlobals import DATA_GROUP

import abc
import pandas as pd
import typing
import time


class dataBase(abc.ABC):
    """
    Base class for data importers for blocks
    """

    def __init__(
        self,
        *args,
        code=None,
        key=None,
        dataType=None,
        indexName=None,
        period=1,
        columnFilter=None,
        upperConstraint=None,
        lowerConstraint=None,
        dayFirst=None,
        parameters={},
        output=None,
        flatten=True,
        **kwargs,
    ):
        super().__init__()

        self.code: str = code
        self.key: str = key
        self.indexName: str = indexName
        self.period: int = period
        self.columnFilter: typing.List[str] = columnFilter
        self.upperConstraint = upperConstraint
        self.lowerConstraint = lowerConstraint
        self.dayFirst: bool = dayFirst
        self.parameters: typing.Dict[typing.Any] = parameters
        self.output: typing.Union[typing.List, typing.Dict[str, str]] = output
        self.flatten: bool = flatten
        # Convert data type to enum
        if dataType is not None:
            try:
                self.dataType: DataSourceTypeEnum = DataSourceTypeEnum[dataType]
            except ValueError:
                mpLogging.warning(
                    "Failed setting data type",
                    description=f"Data Type: {dataType}",
                    group=DATA_GROUP,
                )
        self.end: bool = False
        self.newCycle: bool = False
        if self.columnFilter is not None and len(self.columnFilter) > 0:
            # convert columnFilter to all lowercase
            # convert columnFilter to set for fast lookup
            self.columnFilter = set([column.lower() for column in self.columnFilter])
        else:
            self.columnFilter = None
        self.last_time = 0

    def dataModifications(self, raw_data: typing.Any) -> dict:
        """
        Does modifications to dictList based on set values data base
        If data is not already a dict then convert it to a dict now
            - if output exists use either the first key or value from output
            - otherwise use the data source code
        """
        if raw_data is not None:
            # set columns to lower
            try:
                raw_data = {k.lower(): v for k, v in raw_data.items()}

                if self.columnFilter is not None:
                    # Must use list here as we're going to be deleting while iterating
                    for col in list(raw_data.keys()):
                        if col not in self.columnFilter:
                            del raw_data[col]
            except AttributeError as _:
                # the return value from the data source function wasn't a dict
                # this isn't an error, so we convert the singular value (hopefully str or num) or list into a dict
                name = self.code
                if self.output:
                    try:
                        name = next(iter(self.output.values()))
                    except AttributeError as _:
                        name = self.output[0]
                raw_data = {name.lower(): raw_data}

        return raw_data

    def hasConstraints(self) -> bool:
        """
        Checks if the dataBase has constraints

        @returns: bool of if it has constraints
        """
        return self.lowerConstraint is not None and self.upperConstraint is not None

    def checkConstraint(self, data: pd.DataFrame) -> DataSourceReturnEnum:
        """
        checks data index based on upper lower constraints

        @param: data - pandas dataframe with index that can be compared to constraints

        @return: if outside of constraint it will return constants.DataSourceReturnEnum.OUTSIDE_CONSTRAINT
                     otherwise return None
        """
        # if data is not pandas or comparison to index doesn't work this will except
        # as this could be called every get Data want to log the except
        try:
            if (
                data.index[0] < self.lowerConstraint
                or data.index[-1] > self.upperConstraint
            ):
                return DataSourceReturnEnum.OUTSIDE_CONSTRAINT
            else:
                return None
        except Exception:
            mpLogging.warning(
                "Exception in check constraint, check constraints were set correctly",
                group=DATA_GROUP,
                description=f"Lower constraint: {self.lowerConstraint} \
                                  Upper Constraint: {self.upperConstraint}",
            )
            return None

    @abc.abstractmethod
    def getData(self):
        """
        abstract method that is normally passed to feeds to get data
        """
        return

    @abc.abstractmethod
    def loadData(self):
        """
        abstract method, sets up data getting object as needed, i.e. dataSim loading data into dataFrame
        """
        return

    def readyToGet(self):
        if time.time() - self.last_time > self.period:
            self.last_time = time.time()
            return True
        return False

    def getDataLogging(self):
        mpLogging.info(
            "Data source getting data",
            description=f"Code: {self.code} with period: {self.period}",
            group=DATA_GROUP,
        )
