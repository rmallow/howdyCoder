from .constants import DataSourceTypeEnum, DataSourceReturnEnum

from ..commonUtil import mpLogging
from ..core.commonGlobals import DATA_GROUP, DataSourceSettings

import abc
import pandas as pd
import typing
import time


class dataBase(abc.ABC):
    """
    Base class for data importers for algos
    """

    def __init__(
        self,
        data_source_settings: DataSourceSettings,
        *args,
        **kwargs,
    ):
        super().__init__()

        self.code: str = data_source_settings.name
        self.key: str = data_source_settings.key
        self.period: int = data_source_settings.period
        # TODO: Adding back in dataSim
        # self.indexName: str = indexName
        self.columnFilter: typing.List[str] = None
        self.upperConstraint = None
        self.lowerConstraint = None
        self.dayFirst: bool = False
        self.parameters: typing.Dict[typing.Any] = {
            k: v.value for k, v in data_source_settings.parameters.items()
        }
        self.output: typing.Union[
            typing.List[str], typing.Dict[str, str]
        ] = data_source_settings.output
        self.flatten: bool = data_source_settings.flatten
        self.single_shot: bool = data_source_settings.single_shot
        # Convert data type to enum
        """ TODO: this dataType is actually type of data NOT type of data source
        if dataType is not None:
            try:
                self.dataType: DataSourceTypeEnum = DataSourceTypeEnum[dataType]
            except ValueError:
                mpLogging.warning(
                    "Failed setting data type",
                    description=f"Data Type: {dataType}",
                    group=DATA_GROUP,
                )
        """
        self.end: bool = False
        self.newCycle: bool = False
        if self.columnFilter is not None and len(self.columnFilter) > 0:
            # convert columnFilter to all lowercase
            # convert columnFilter to set for fast lookup
            self.columnFilter = set([column.lower() for column in self.columnFilter])
        else:
            self.columnFilter = None
        self.last_time = 0
        self.just_started = True

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
        if (not self.single_shot and time.time() - self.last_time > self.period) or (
            self.single_shot and self.just_started
        ):
            self.last_time = time.time()
            self.just_started = False
            return True
        return False

    def getDataLogging(self):
        mpLogging.info(
            "Data source getting data",
            description=f"Code: {self.code} with period: {self.period}",
            group=DATA_GROUP,
        )
