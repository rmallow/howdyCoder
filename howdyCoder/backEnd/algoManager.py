from .block import block
from . import actionFactory as aF
from .feed import feed
from .dataBase import dataBase
from . import dataSourceFactory as dF
from . import messageRouter as mRModule
from ..commonUtil import mpLogging

from ..commonUtil import configLoader
from ..commonUtil import userFuncCaller

from ..core.configConstants import (
    ActionTypeEnum,
)
from ..core.commonGlobals import (
    ActionSettings,
    AlgoSettings,
    SETUP_FUNCS,
    DataSourceSettings,
)

import copy
import typing

from dataclass_wizard import fromdict


class AlgoManager:
    def __init__(self):
        self.blocks = {}
        # self.messageRouter = messageRouter
        self.columnNames = []

    def loadBlock(self, config_dict: dict) -> None:
        return [self._loadBlockAndDataSource(config_dict)]

    def _loadBlockAndDataSource(self, original_config: dict) -> block:
        dataSources = []
        func_replaced_config = copy.deepcopy(original_config)
        user_funcs = self.replaceFunctions(func_replaced_config)
        algo_settings = fromdict(AlgoSettings, func_replaced_config)
        dataSources = self._loadDataSources(algo_settings.data_sources)
        feed = self._loadFeed(dataSources)
        actionList = self._loadActionList(algo_settings.action_list, feed)
        blk = block(
            actionList,
            feed,
            algo_settings,
            user_funcs,
            code=algo_settings.name,
        )
        # we're setting up the column names in action list and we use that for sending to the ui
        # so the column names can be selected for viewing there, should change later
        blk.columnNames = self.columnNames
        self.blocks[algo_settings.name] = blk
        return blk

    def _loadDataSources(
        self, data_source_settings: typing.Dict[str, DataSourceSettings]
    ) -> list[dataBase]:
        dataSources = []
        for _, config in data_source_settings.items():
            dataSources.append(self._loadDataSource(config))
        return dataSources

    def _loadDataSource(self, data_source_settings: DataSourceSettings) -> dataBase:
        # use the dataSourceFactory with the type to create the dataSource
        factory = dF.dataSourceFactory()
        return factory.create(data_source_settings, data_source_settings.type_)

    def _loadActionList(
        self, action_list_settings: typing.Dict[str, ActionSettings], feed
    ) -> list:
        actionList = []
        factory = aF.actionFactory()
        for name, action_settings in action_list_settings.items():
            creator_type = action_settings.type_
            if action_settings.aggregate:
                creator_type = action_settings.aggregate + action_settings.type_
            action = factory.create(action_settings, creator_type)
            # if it is an event but not an aggregate then add the name to column names
            # so it can be selected later
            if (
                creator_type == ActionTypeEnum.EVENT.display
                and not action_settings.aggregate
            ):
                self.columnNames.append(name)
            action.feed = feed
            actionList.append(action)
        return actionList

    def _loadFeed(self, dataSources: list[dataBase]) -> feed:
        return feed(dataSources)

    def replaceFunctions(self, config_copy):
        user_funcs = []

        def assignUserFuncCaller(c, k, v):
            nonlocal user_funcs
            if v is not None:
                user_funcs.append(userFuncCaller.UserFuncCaller(**v))
                c[k]["user_func"] = user_funcs[-1]

        configLoader.dfsConfigDict(
            config_copy,
            lambda k: k.lower().endswith("func"),
            assignUserFuncCaller,
        )

        configLoader.dfsConfigDict(
            config_copy,
            lambda k: k == SETUP_FUNCS,
            lambda _1, _2, v: (
                assignUserFuncCaller(f_name, f_value) for f_name, f_value in v.items()
            ),
        )
        return user_funcs
