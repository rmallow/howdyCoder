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
    DATA_SOURCES,
    NAME,
    TYPE,
    ACTION_LIST,
    AGGREGATE,
    SETUP_FUNCS,
    ActionTypeEnum,
)

import copy


class AlgoManager:
    # TODO: Either remove or reimplement message router / handlers
    # def __init__(self, messageRouter: mRModule.messageRouter):
    def __init__(self):
        self.blocks = {}
        self.dataMangerList = {}
        # self.messageRouter = messageRouter
        self.columnNames = []

    def loadItem(self, configDict: dict) -> None:
        self.loadBlocks(configDict)

    def loadBlocks(self, configDict: dict) -> None:
        mpLogging.info("---- Block Manager Loading Blocks ----")
        ret_blocks = []
        for code, config in configDict.items():
            mpLogging.info("Loading Block with code: " + code)
            ret_blocks.append(self._loadBlockAndDataSource(config, code))
            self.columnNames = []
        mpLogging.info("---- Block Manager Done Loading ----")
        return ret_blocks

    def _loadBlockAndDataSource(self, original_config: dict, code: str) -> block:
        dataSources = []
        func_replaced_config = copy.deepcopy(original_config)
        user_funcs = self.replaceFunctions(func_replaced_config)
        dataSources = self._loadDataSources(func_replaced_config[DATA_SOURCES])
        feed = self._loadFeed(dataSources)
        actionList = self._loadActionList(func_replaced_config[ACTION_LIST], feed)
        # TODO: Either remove or reimplement message router / handlers
        """
        blk = block(
            actionList,
            feed,
            self.messageRouter,
            original_config,
            user_funcs,
            code=code,
        )"""
        blk = block(
            actionList,
            feed,
            original_config,
            user_funcs,
            code=code,
        )
        # we're setting up the column names in action list and we use that for sending to the ui
        # so the column names can be selected for viewing there, should change later
        blk.columnNames = self.columnNames
        self.blocks[code] = blk
        self.dataMangerList[code] = dataSources
        return blk

    def _loadDataSources(self, dataSourcesConfig: dict) -> list[dataBase]:
        dataSources = []
        for code, config in dataSourcesConfig.items():
            config["code"] = code
            dataSources.append(self._loadDataSource(config))
        return dataSources

    def _loadDataSource(self, dataSourceConfig: dict) -> dataBase:
        dataSourceType = dataSourceConfig[TYPE]
        if "constraint" in dataSourceConfig:
            dataSourceConfig |= dataSourceConfig["constraint"]

        # use the dataSourceFactory with the type to create the dataSource
        factory = dF.dataSourceFactory()
        return factory.create(dataSourceConfig, dataSourceType)

    def _loadActionList(self, actionListConfig: dict, feed) -> list:
        actionList = []
        factory = aF.actionFactory()
        for name, actionConfig in actionListConfig.items():
            creatorType = actionConfig[TYPE]
            if AGGREGATE in actionConfig:
                creatorType = AGGREGATE + actionConfig[AGGREGATE]
            actionConfig[NAME] = name
            action = factory.create(actionConfig, creatorType)
            # if it is an event but not an aggregate then add the name to column names
            # so it can be selected later
            if (
                creatorType == ActionTypeEnum.EVENT.display
                and AGGREGATE not in actionConfig
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
            user_funcs.append(userFuncCaller.userFuncCaller(**v))
            c[k] = user_funcs[-1]

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
