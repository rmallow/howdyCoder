from ..core.dataStructs import ProgramStatusData, InputData, Modes
from .actionPool import ActionPool
from ..core import message as msg
from ..core import messageKey as msgKey
from . import constants as con
from .feed import feed
from .program import Program


from ..commonUtil import mpLogging
from ..commonUtil.repeatTimer import setInterval
from ..core.commonGlobals import ALGO_GROUP, BACKTRACK, ProgramTypes

import time


class Algo(Program):
    def __init__(
        self,
        actionList,
        feed_obj,
        config,
        user_funcs,
        *args,
        **kwargs,
    ):
        super().__init__(config, user_funcs, *args, **kwargs)
        self.feed_obj: feed = feed_obj
        self.pool = ActionPool(actionList)
        self.track = False
        self.feed_last_update_time = 0
        self.period = feed_obj.period
        self.type_ = ProgramTypes.ALGO

        self.addCmdFunc(msg.CommandType.ADD_OUTPUT_VIEW, Algo.addOutputView)
        self.addCmdFunc(msg.CommandType.EXPORT, Algo.exportData)
        self.addCmdFunc(msg.CommandType.ADD_INPUT_DATA, Algo.addInputData)

    def update(self):
        feed_ret_val = self.feed_obj.update()
        self.feed_last_update_time = time.time()
        if feed_ret_val is not None:
            if feed_ret_val == con.FeedRetValues.VALID_VALUES:
                self.pool.doActions()
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
        self.feed_obj.started()

    def addInputData(self, _, details=None):
        if details is not None:
            input_data = InputData(**details)
            self.feed_obj.addInputData(input_data.data_source_name, input_data.val)
