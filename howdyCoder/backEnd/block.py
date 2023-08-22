from .actionPool import actionPool
from ..core import message as msg
from ..core import messageKey as msgKey
from . import constants as con
from .feed import feed

from .util.commandProcessor import commandProcessor

from ..commonUtil import mpLogging
from ..commonUtil.repeatTimer import setInterval
from ..commonUtil import userFuncCaller
from ..core.commonGlobals import (
    BLOCK_GROUP,
    BACKTRACK,
    FUNC_GROUP,
    AlgoStatusData,
    Modes,
)
from ..commonUtil import queueManager as qm

from dataclasses import asdict
import time
import typing
import threading


BLOCK_QUEUE_CHECK_TIMER = 0.5


class block(commandProcessor):
    def __init__(
        self,
        actionList,
        feed_obj,
        config,
        user_funcs,
        *args,
        code="algo1",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.code = code
        self._end = False
        self.feed_obj: feed = feed_obj
        self.pool = actionPool(actionList, self.code)
        self.config = config
        self._user_funcs: typing.List[userFuncCaller.userFuncCaller] = user_funcs
        self._mainframe_queue = None
        self.block_queue = None
        self.track = False
        self.feed_last_update_time = 0
        self.check_block_status_event: threading.Event = None
        self.feed_update_event: threading.Event = None
        self.start_time: float = None

        self.addCmdFunc(msg.CommandType.ADD_OUTPUT_VIEW, block.addOutputView)
        self.addCmdFunc(msg.CommandType.CHECK_STATUS, block.checkStatus)
        self.addCmdFunc(msg.CommandType.EXPORT, block.exportData)

    @setInterval(BLOCK_QUEUE_CHECK_TIMER)
    def checkblock_queue(self):
        # Check if there are messages for the block to process
        if not self._end and self.block_queue is not None:
            # This will block the block until the queue is cleared so need to avoid
            # spamming this with commands
            while not self._end and not self.block_queue.empty():
                # Use the command processor way of handling command messages
                command_message = self.block_queue.get()
                if (
                    command_message
                    and command_message.messageType == msg.MessageType.COMMAND
                ):
                    self.processCommand(
                        command_message.content, details=command_message.details
                    )

    @setInterval(1)
    def updateFeed(self):
        if self._current_mode == Modes.STARTED:
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
                    # Want to do nothing and process potential block messages
                    pass
                elif feed_ret_val != con.DataSourceReturnEnum.END_DATA:
                    # Feed is at end of data so don't want to keep calling it
                    self._current_mode = Modes.STOPPED
                else:
                    # Feeds should not be returning None, issue a warning and stop updating
                    mpLogging.warning(
                        "Block "
                        + str(self.code)
                        + " received invalid return value from feed",
                        group=BLOCK_GROUP,
                        description="Return recognized enum value for feed status",
                    )
                    self._current_mode = Modes.STOPPED

    def start(self, isLocal):
        # call user funcs setup now that we are in our own process
        for uF in self._user_funcs:
            # if any of the user funcs fail to setup we'll end now
            if not uF.setup():
                mpLogging.critical(
                    "Function setup failed, function not found, block process exiting early",
                    description=f"userFunc: {uF.name}, block: {self.code}",
                    group=FUNC_GROUP,
                )
                self._end = True
                return
        # Connect to clientServerManager
        self._clientSeverManager = qm.createQueueManager(isLocal)
        self._clientSeverManager.connect()
        assert hasattr(self._clientSeverManager, qm.GET_MAINFRAME_QUEUE)
        self._mainframe_queue = getattr(
            self._clientSeverManager, qm.GET_MAINFRAME_QUEUE
        )()
        self._current_mode = Modes.STARTED
        self.start_time = time.time()
        self.check_block_status_event = self.checkblock_queue(timer=True)
        # can only set the interval time when we get the period off feed obj
        self.feed_update_event = self.updateFeed(
            timer=True, on_runtime_time=self.feed_obj.period
        )

        while not self._end:
            """
            Need to keep the main thread open, so we'll sleep here and make sure it's supposed to still
            be open every 10 seconds, if we close this thread, it will cut off communication with mainframe
            """
            time.sleep(10)

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
            content=msg.UiUpdateType.BLOCK,
            details=self.feed_obj.getNewCombinedDataOfLength(length, ignore_last_sent),
            key=msgKey.messageKey(self.code, None),
        )
        self._mainframe_queue.put(m)

    def checkStatus(self, _, details):
        """
        Aside from special cases like COLUMNS, the details on this message will be displayed on the status window
        """
        status_data = AlgoStatusData(
            0.0,
            time.time(),
            self.feed_obj.getDataLength(),
            self.feed_last_update_time,
            time.time() - self.start_time,
            list(self.feed_obj.data.keys()) + list(self.feed_obj.calcData.keys()),
            self._current_mode,
        )
        if details is not None and isinstance(details, dict):
            status_data.send_time = AlgoStatusData(**details).send_time

        returnMessage = msg.message(
            msg.MessageType.UI_UPDATE,
            msg.UiUpdateType.STATUS,
            key=msgKey.messageKey(self.code, None),
            details=asdict(status_data),
        )
        self._mainframe_queue.put(returnMessage)

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

    def cmdShutdown(self, command, details=None):
        self._end = True
