from . import constants as con
from . import feed as feedModule

from ..commonUtil.userFuncCaller import UserFuncCaller
from ..commonUtil import mpLogging, helpers
from ..core.commonGlobals import FIRST, DATA_SET, ActionSettings
from ..core.configConstants import ActionDataType, ENUM_DISPLAY
from ..commonUtil import sparseDictList

import bisect
import typing
import pandas as pd


def findData(feed: feedModule.feed, col: str) -> typing.List[sparseDictList.SparseData]:
    """
    Find the specified column from feed

    Arg:
        feed:
            feed data structures on which to serach for column
        col:
            string name of column to find

    Returns:
        DictList specified column or None if not found

    """
    if feed.data is not None and col in feed.data:
        return feed.data[col]
    elif feed.calcData is not None and col in feed.calcData:
        return feed.calcData[col]
    return None


class action:
    """
    Base virtual class for actions used by action pool

    Attributes:
        actionType:
            used for easier recreation of action, details which of child classes the action is
            passed in as type, as it makes more sense in the config files to be listed as type
        calcFunc:
            called to produce ouptut values for the action
        period:
            interger number of data units to use for data set in calc func
        name:
            string given to the action from the config
        parameters:
            values passed into calcfunc, come from config or setupFuncs
        setupFuncs:
            add to parameters, run one time on startup
        aggregate:
            bool for if action is aggregate or not
    """

    def __init__(
        self,
        action_settings: ActionSettings,
        *args,
        **kwargs,
    ):
        self.actionType: str = action_settings.type_
        self.calcFunc: UserFuncCaller = action_settings.calc_func.user_func
        self.name: str = action_settings.name.lower()
        self.parameters: dict = action_settings.parameters
        self.setupFuncs: typing.Dict[str, UserFuncCaller] = action_settings.setup_funcs
        self.aggregate: bool = action_settings.aggregate
        self.input_info_map = action_settings.input_

        self.action_data_type: ActionDataType = helpers.findEnumByAttribute(
            ActionDataType, ENUM_DISPLAY, action_settings.input_data_type
        )
        self.flatten: bool = action_settings.flatten

        self.input = [x.lower() for x in self.input_info_map.keys()]

        self.last_used = {i: None for i in self.input}

        self.dataSet: pd.DataFrame = None
        # this must be set before calling update
        self.lastCalcIndex: int = None
        self.isFirst: bool = True
        self.feed: feedModule.feed = None

    def update(self):
        """Called by action pool, updates dataSet and calls calcFunc"""
        indexing_input, index_length = self.checkInput()
        if indexing_input:
            for x in range(index_length):
                index = findData(self.feed, indexing_input)[-(index_length - x)].index
                self.updateDataSet(index)

                self.parameters[FIRST] = self.isFirst
                self.isFirst = False
                yield self.calcFunc(**self.parameters), index

    def checkInput(self) -> typing.Tuple[str, int]:
        """
        Check to see if we have enough input data to perform calculations and if so, determine how many calculations

        If there is a requires_new column, the minimum new data in a requirew_new column will override at the end
        """
        indexing_input = ""
        cur_index_length = None
        for input_name in self.input:
            if data := findData(self.feed, input_name):
                after_old = 0
                if self.last_used[input_name] is None:
                    if len(data) < self.period:
                        return "", 0
                    after_old = len(data) - self.period + 1
                elif len(data) > self.last_used[input_name]:
                    after_old = len(data) - self.last_used[input_name]
                if (
                    input_name in self.requires_new
                    and (cur_index_length is None or after_old < cur_index_length)
                ) or (
                    not self.requires_new
                    and (cur_index_length is None or after_old > cur_index_length)
                ):
                    indexing_input = input_name
                    cur_index_length = after_old
            else:
                return "", 0
        return indexing_input, cur_index_length

    def updateDataSet(self, end_index: int):
        """Called by updates, updates dataSet by finding necessary columns and adding appropriate slices of them"""
        temp_data_set = {}
        for col in self.input:
            data = findData(self.feed, col)
            data_arr_index = bisect.bisect_right(
                data, end_index, key=lambda sparse_data: sparse_data.index
            )
            value_only_data = [
                data[x].value
                for x in range(
                    max(data_arr_index - self.period, 0),
                    max(data_arr_index, self.period),
                )
            ]
            temp_data_set[
                self.labels[col] if col in self.labels else col
            ] = value_only_data
            self.last_used[col] = max(
                self.last_used[col] if self.last_used[col] is not None else 0,
                data_arr_index,
            )

        # create the datset to be used for the calcFunc
        if self.action_data_type == ActionDataType.DATA_FRAME:
            self.dataSet = pd.DataFrame(temp_data_set)
        elif self.action_data_type == ActionDataType.LISTS_OF_LISTS:
            # order is preserved
            self.dataSet = [v for v in temp_data_set.values()]
        else:
            self.dataSet = temp_data_set
        self.parameters[DATA_SET] = self.dataSet

    def setup(self):
        """Called on action initialization, this setup function is supplied from the config"""
        if self.parameters is None or not isinstance(self.parameters, dict):
            self.parameters = {}

        for key, userFunc in self.setupFuncs.items():
            self.parameters |= {key: userFunc(**self.parameters)}
