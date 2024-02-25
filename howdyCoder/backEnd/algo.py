from .actionPool import ActionPool
from . import constants as con
from .feed import feed
from .program import Program

from ..core import message as msg
from ..core import messageKey as msgKey
from ..core.dataStructs import (
    ActionSettings,
    AlgoSettings,
    DataSourceSettings,
    ProgramSettings,
    SourceData,
    Modes,
)


from . import dataSourceFactory as dF
from .dataBase import dataBase
from . import actionFactory as aF
from .action import Action

from ..commonUtil import mpLogging
from ..core.commonGlobals import ALGO_GROUP, BACKTRACK, ProgramTypes, ActionTypeEnum
from ..core import topoSort

import typing
import time
import copy
from dataclass_wizard import fromdict, asdict


class Algo(Program):
    def __init__(
        self,
        is_local: bool,
        settings: ProgramSettings,
        *args,
        **kwargs,
    ):
        super().__init__(is_local, settings, *args, **kwargs)
        # setup base variables
        self.track = False
        self.feed_last_update_time = 0
        self.type_ = ProgramTypes.ALGO
        self.column_names = []

        # construct sub items
        self.loadSettings(settings)

        self.addCmdFunc(msg.CommandType.ADD_OUTPUT_VIEW, Algo.addOutputView)
        self.addCmdFunc(msg.CommandType.EXPORT, Algo.exportData)
        self.addCmdFunc(msg.CommandType.ADD_SOURCE_DATA, Algo.addSourceData)

        self.start()

    def _loadDataSource(self, data_source_settings: DataSourceSettings) -> dataBase:
        # use the dataSourceFactory with the type to create the dataSource
        factory = dF.dataSourceFactory()
        return factory.create(data_source_settings, data_source_settings.type_)

    def _loadDataSources(
        self, data_source_settings: typing.Dict[str, DataSourceSettings]
    ) -> list[dataBase]:
        dataSources = []
        for _, config in data_source_settings.items():
            dataSources.append(self._loadDataSource(config))
        return dataSources

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
                self.column_names.append(name)
            action.feed = feed
            action_dict[name] = action
        return ActionPool(action_dict, topo_levels=topo_levels)

    def loadSettings(self, settings: ProgramSettings):
        func_replaced_config = copy.deepcopy(asdict(settings))
        self._user_funcs = self.addUserFuncs(func_replaced_config)
        algo_settings_with_user_funcs: AlgoSettings = fromdict(
            ProgramSettings, func_replaced_config
        ).settings

        dataSources = self._loadDataSources(algo_settings_with_user_funcs.data_sources)
        self.feed_obj: feed = feed(dataSources)
        self.period = self.feed_obj.period

        topo_levels, _, _ = topoSort.getTopoSort(settings.settings)
        self.action_pool = self._loadActionPool(
            algo_settings_with_user_funcs.action_list, self.feed_obj, topo_levels
        )

    def update(self):
        feed_ret_val = self.feed_obj.update()
        self.feed_last_update_time = time.time()
        if feed_ret_val is not None:
            if feed_ret_val == con.FeedRetValues.VALID_VALUES:
                self.doActions()
                if self.track:
                    self.sendCombinedData()
            elif feed_ret_val == con.FeedRetValues.NO_VALID_VALUES:
                pass
            elif feed_ret_val == con.DataSourceReturnEnum.OUTSIDE_CONSTRAINT:
                self.clear()
            elif feed_ret_val == con.DataSourceReturnEnum.NO_DATA:
                # Want to do nothing and process potential algos messages
                pass
            elif feed_ret_val != con.DataSourceReturnEnum.END_DATA:
                # Feed is at end of data so don't want to keep calling it
                self._current_mode = Modes.STOPPED
            else:
                # Feeds should not be returning None, issue a warning and stop updating
                mpLogging.warning(
                    f"Algo {self.code} eceived invalid return value from feed",
                    group=ALGO_GROUP,
                    description="Return recognized enum value for feed status",
                )
                self._current_mode = Modes.STOPPED

    def clear(self):
        self.feed_obj.clear()

    def addOutputView(self, _, details=None):
        self.track = True
        # can only backtrack if data already exists
        if self.feed_obj.data is not None:
            if details and BACKTRACK in details and details[BACKTRACK] != 0:
                # if backtrack is present and is not 0 then send back to mainframed
                # the desired amount of data
                backtrack_length = details[BACKTRACK]
                if backtrack_length == -1:
                    # if back track is -1 then send all of the data available
                    backtrack_length = self.feed_obj.getDataLength()
                self.sendCombinedData(length=backtrack_length, ignore_last_sent=True)

    def sendCombinedData(self, length=None, ignore_last_sent=False):
        """
        Combine the data of calc and data member objects and pack into a message to send
        """
        # need to check lengths on both, we want length to the be the shorter of the two
        if length is not None and length > self.feed_obj.getDataLength():
            length = self.feed_obj.getDataLength()
        m = msg.message(
            msg.MessageType.UI_UPDATE,
            content=msg.UiUpdateType.ALGO,
            details=self.feed_obj.getNewCombinedDataOfLength(length, ignore_last_sent),
            key=msgKey.messageKey(self.code, None),
        )
        self._mainframe_queue.put(m)

    def populateTypeSpecificStatusData(self, details, status_data):
        """
        Aside from special cases like COLUMNS, the details on this message will be displayed on the status window
        """
        status_data.data_length = self.feed_obj.getDataLength()
        status_data.feed_last_update_time = self.feed_last_update_time
        status_data.columns = list(self.feed_obj.data.keys()) + list(
            self.feed_obj.calcData.keys()
        )

    def exportData(self, _, details):
        self._mainframe_queue.put(
            msg.message(
                msg.MessageType.UI_UPDATE,
                msg.UiUpdateType.EXPORT,
                key=msgKey.messageKey(self.code, None),
                details=self.feed_obj.getAllData(),
            )
        )

    def cmdStart(self, command, details=None):
        super().cmdStart(command, details)
        self.feed_obj.started()

    def addSourceData(self, _, details=None):
        if details is not None:
            input_data = SourceData(**details)
            self.feed_obj.addSourceData(input_data.data_source_name, input_data.val)
