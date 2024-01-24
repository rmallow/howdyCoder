from ..core.dataStructs import (
    ActionSettings,
    AlgoSettings,
    DataSourceSettings,
    ProgramSettings,
)
from .algo import Algo
from . import actionFactory as aF
from .feed import feed
from .dataBase import dataBase
from . import dataSourceFactory as dF
from .actionPool import ActionPool
from .action import Action

from ..core.commonGlobals import ActionTypeEnum, ENUM_DISPLAY
from ..core import topoSort

import copy
import typing

from dataclass_wizard import fromdict, asdict
from .programManager import ProgramManager


class AlgoManager(ProgramManager):
    def __init__(self):
        super().__init__()
        self.columnNames = []

    def load(self, program_settings: ProgramSettings) -> Algo:
        dataSources = []
        func_replaced_config = copy.deepcopy(asdict(program_settings))
        user_funcs = self.addUserFuncs(func_replaced_config)
        algo_settings_with_user_funcs: AlgoSettings = fromdict(
            ProgramSettings, func_replaced_config
        ).settings
        dataSources = self._loadDataSources(algo_settings_with_user_funcs.data_sources)
        feed = self._loadFeed(dataSources)
        topo_levels, _, _ = topoSort.getTopoSort(program_settings.settings)
        action_pool = self._loadActionPool(
            algo_settings_with_user_funcs.action_list, feed, topo_levels
        )
        algo = Algo(
            action_pool,
            feed,
            program_settings,
            user_funcs,
        )
        # we're setting up the column names in action list and we use that for sending to the ui
        # so the column names can be selected for viewing there, should change later
        algo.columnNames = self.columnNames
        self.programs[algo_settings_with_user_funcs.name] = algo
        return algo

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

    def _loadActionPool(
        self,
        action_list_settings: typing.Dict[str, ActionSettings],
        feed,
        topo_levels: typing.List[typing.List[str]],
    ) -> list:
        action_dict: typing.Dict[str, Action] = {}
        factory = aF.actionFactory()
        for name, action_settings in action_list_settings.items():
            creator_type = action_settings.type_
            if action_settings.aggregate:
                creator_type = action_settings.aggregate + action_settings.type_
            action = factory.create(action_settings, creator_type)
            # if it is an event but not an aggregate then add the name to column names
            # so it can be selected later
            if (
                creator_type == ActionTypeEnum.EVENT.value
                and not action_settings.aggregate
            ):
                self.columnNames.append(name)
            action.feed = feed
            action_dict[name] = action
        return ActionPool(action_dict, topo_levels=topo_levels)

    def _loadFeed(self, dataSources: list[dataBase]) -> feed:
        return feed(dataSources)
