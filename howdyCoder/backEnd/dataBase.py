from ..core.dataStructs import DataSourceSettings, Modes
from ..commonUtil import mpLogging
from ..core.commonGlobals import DATA_GROUP, EditorType
from ..core.modeHandler import ModeHandler

import abc
import pandas as pd
import typing
import time


class DataBase(ModeHandler):
    """
    Base class for data importers for algos
    """

    def __init__(
        self,
        data_source_settings: DataSourceSettings,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.code: str = data_source_settings.name
        self.key: str = data_source_settings.key
        self.period: int = data_source_settings.period
        self.data_in_rows: bool = data_source_settings.data_in_rows

        self.columnFilter: typing.List[str] = None
        self.upperConstraint = None
        self.lowerConstraint = None
        self.dayFirst: bool = False
        self.parameters: typing.Dict[str, typing.Any] = {
            v.name: v.value
            for v in data_source_settings.parameters.values()
            if v.type_ != EditorType.FUNC.display
        }
        self.output: typing.Union[typing.List[str], typing.Dict[str, str]] = (
            data_source_settings.output
        )
        self.flatten: bool = data_source_settings.flatten
        self.single_shot: bool = data_source_settings.single_shot

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

    def getData(self):
        """Call child class get if ready to get and change mode afterward if singleshot"""
        ret_val = None
        if self.readyToGet():
            ret_val = self._getData()
        if self.single_shot and self.getMode() == Modes.RUNNING:
            self.changeMode(Modes.FINISHED)
        return ret_val

    @abc.abstractmethod
    def _getData(self):
        """
        abstract method implemented by base class for actually getting the data
        """
        pass

    @abc.abstractmethod
    def loadData(self):
        """
        abstract method, sets up data getting object as needed, i.e. loading data into dataFrame
        """
        return

    def readyToGet(self):
        if self.getMode() == Modes.RUNNING and (
            time.time() - self.last_time > self.period or self.single_shot
        ):
            self.last_time = time.time()
            return True
        return False

    def getDataLogging(self):
        mpLogging.info(
            "Data source getting data",
            description=f"Code: {self.code} with period: {self.period}",
            group=DATA_GROUP,
        )

    def onRunning(self, old_mode: Modes) -> None:
        super().onRunning(old_mode)
        self.loadData()
