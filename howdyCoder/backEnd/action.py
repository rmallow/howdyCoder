from ..core.dataStructs import ActionSettings, InputSettings
from . import feed as feedModule

from ..commonUtil.userFuncCaller import UserFuncCaller
from ..commonUtil import helpers
from ..core.commonGlobals import (
    FIRST,
    DATA_SET,
    ActionDataType,
    ENUM_DISPLAY,
    EditorType,
)
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


class Action:
    """
    Base virtual class for actions used by action pool
    """

    def __init__(
        self,
        action_settings: ActionSettings,
        *args,
        **kwargs,
    ):
        self.actionType: str = action_settings.type_
        self.calcFunc: UserFuncCaller = action_settings.calc_function.user_function
        self.name: str = action_settings.name.lower()
        self.parameters: typing.Dict[str, typing.Any] = {
            v.name: v.value
            for v in action_settings.parameters.values()
            if v.type_ != EditorType.FUNC.display
        }
        self.setup_funcs: typing.Dict[str, typing.Any] = {
            v.name: v.value
            for v in action_settings.parameters.values()
            if v.type_ == EditorType.FUNC.display
        }

        self._calc_internal_setup_functions = (
            action_settings.calc_function.internal_setup_functions
        )

        self.is_first: bool = True
        self.aggregate: bool = action_settings.aggregate
        self.flatten: bool = action_settings.flatten
        self.transpose: bool = action_settings.transpose
        self.single_shot: bool = action_settings.single_shot
        self.feed: feedModule.feed = None
        self.just_started = False

        # some actions might not take any input from the feed
        self.input_info_map: typing.Dict[str, InputSettings] = {
            k.lower(): v for k, v in action_settings.input_.items()
        }
        if self.input_info_map:
            self.any_requires_new = any(
                v.requires_new for v in self.input_info_map.values()
            )

            self.action_data_type: ActionDataType = helpers.findEnumByAttribute(
                ActionDataType, ENUM_DISPLAY, action_settings.input_data_type
            )

            self.input = [x.lower() for x in self.input_info_map.keys()]

            self.last_used = {i: None for i in self.input}

            self.dataSet: pd.DataFrame = None
            # this must be set before calling update
            self.lastCalcIndex: int = None

    def multipleUpdate(self):
        """
        Called by action pool, updates dataSet and calls calcFunc
        This is a yield so only works when called in a generator type situation
        """
        indexing_input, index_length = self.checkInput()
        if indexing_input:
            for x in range(index_length):
                index = findData(self.feed, indexing_input)[-(index_length - x)].index
                self.updateDataSet(index)

                self.parameters[FIRST] = self.is_first
                self.is_first = False
                val, stdout_str, stderr_str = self.calcFunc(
                    **self.parameters, _caller_name=f"Action: {self.name}"
                )
                yield val, stdout_str, stderr_str, index

    def update(self):
        if self.just_started or not self.single_shot:
            self.just_started = False
            self.parameters[FIRST] = self.is_first
            self.is_first = False
            _, stdout_str, stderr_str = self.calcFunc(**self.parameters)
            return [stdout_str], [stderr_str]
        return [], []

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
                if self.input_info_map[input_name].period == -1:
                    if len(data) > 0:
                        after_old = 1
                    else:
                        return "", 0
                else:
                    if self.last_used[input_name] is None:
                        if len(data) < self.input_info_map[input_name].period:
                            return "", 0
                        after_old = (
                            len(data) - self.input_info_map[input_name].period + 1
                        )
                    elif len(data) > self.last_used[input_name]:
                        after_old = len(data) - self.last_used[input_name]
                if (
                    self.input_info_map[input_name].requires_new
                    and (cur_index_length is None or after_old < cur_index_length)
                ) or (
                    not self.any_requires_new
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
            lo = max(data_arr_index - self.input_info_map[col].period, 0)
            hi = max(data_arr_index, self.input_info_map[col].period)
            if self.input_info_map[col].period == -1:
                lo, hi = 0, data_arr_index
            value_only_data = [data[x].value for x in range(lo, hi)]
            temp_data_set[
                self.input_info_map[col].name if self.input_info_map[col].name else col
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

        for key, function_settings in self.setup_funcs.items():
            self.parameters |= {
                key: function_settings.user_function(**self.parameters)[0]
            }

        for func_name, parm_name in self._calc_internal_setup_functions.items():
            self.parameters |= {
                parm_name: self.calcFunc.callFunc(func_name, **self.parameters)[0]
            }
