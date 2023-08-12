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
        feedObj,
        config,
        user_funcs,
        *args,
        code="algo1",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.code = code
        self.end = False
        self.feedObj: feed = feedObj
        # TODO: Either remove or reimplement message router / handlers
        # self.messageRouter = messageRouter
        # self.pool = actionPool(actionList, messageRouter, self.code)
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

    @setInterval(BLOCK_QUEUE_CHECK_TIMER)
    def checkblock_queue(self):
        # Check if there are messages for the block to process
        if self.block_queue is not None:
            # This will block the block until the queue is cleared so need to avoid
            # spamming this with commands
            while not self.block_queue.empty():
                # Use the command processor way of handling command messages
                commandMessage = self.block_queue.get()
                if commandMessage.messageType == msg.MessageType.COMMAND:
                    self.processCommand(
                        commandMessage.content, details=commandMessage.details
                    )

    @setInterval(1)
    def updateFeed(self):
        if self._current_mode == Modes.STARTED:
            feed_ret_val = self.feedObj.update()
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
                self.end = True
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
            timer=True, on_runtime_time=self.feedObj.period
        )

        while not self.end:
            """
            Need to keep the main thread open, so we'll sleep here and make sure it's supposed to still
            be open every 10 seconds, if we close this thread, it will cut off communication with mainframe
            """
            time.sleep(10)

    def clear(self):
        self.feedObj.clear()
        # time is set as None as it won't be needed by message router
        message = msg.message(
            msg.MessageType.COMMAND,
            msg.CommandType.CLEAR,
            key=msgKey.messageKey(self.code, None),
        )

        # TODO: Either remove or reimplement message router / handlers
        # self.messageRouter.receive(message)

    def addOutputView(self, _, details=None):
        self.track = True
        # can only backtrack if data already exists
        if self.feedObj.data is not None:
            if details and BACKTRACK in details and details[BACKTRACK] != 0:
                # if backtrack is present and is not 0 then send back to mainframed
                # the desired amount of data
                backtrackLength = details[BACKTRACK]
                if backtrackLength == -1:
                    # if back track is -1 then send all of the data available
                    backtrackLength = self.feedObj.getDataLength()
                self.sendCombinedData(backtrackLength)

    def sendCombinedData(self, length=None):
        """
        Combine the data of calc and data member objects and pack into a message to send
        """
        # need to check lengths on both, we want length to the be the shorter of the two
        if length is not None and length > self.feedObj.getDataLength():
            length = self.feedObj.getDataLength()
        m = msg.message(
            msg.MessageType.UI_UPDATE,
            content=msg.UiUpdateType.BLOCK,
            details=self.feedObj.getNewCombinedDataOfLength(length),
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
            self.feedObj.getDataLength(),
            self.feed_last_update_time,
            time.time() - self.start_time,
            list(self.feedObj.data.keys()) + list(self.feedObj.calcData.keys()),
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
