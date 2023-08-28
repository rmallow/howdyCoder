from ..commonUtil.multiBase import multiBase
from ..commonUtil.userFuncCaller import UserFuncCaller
from ..core import message as msg
from ..core import messageKey as msgKey
from ..commonUtil import mpLogging
from ..commonUtil.repeatTimer import setInterval
from ..commonUtil import queueManager as qm
from ..core.commonGlobals import (
    FUNC_GROUP,
    Modes,
    ProgramStatusData,
    ProgramSettings,
    ProgramTypes,
)

from .util.commandProcessor import commandProcessor

from abc import ABC, abstractmethod
import time
import typing
from dataclasses import asdict
import threading

PROGRAM_QUEUE_CHECK_TIMER = 0.5


class Program(commandProcessor, ABC):
    def __init__(self, config, user_funcs):
        super().__init__()
        self._end = False
        self.config: ProgramSettings = config
        self.program_queue = None
        self._user_funcs: typing.List[UserFuncCaller] = user_funcs
        self._mainframe_queue = None
        self.start_time: float = None
        self.period = 1
        self.type_ = ProgramTypes.PROGRAM

        self.check_program_status_event: threading.Event = None
        self.feed_update_event: threading.Event = None

        self.addCmdFunc(msg.CommandType.CHECK_STATUS, Program.checkStatus)

    def getQueue(self):
        return self.program_queue

    def setQueue(self, queue):
        self.program_queue = queue

    def keepAlive(self):
        while not self._end:
            """
            Need to keep the main thread open, so we'll sleep here and make sure it's supposed to still
            be open every 10 seconds, if we close this thread, it will cut off communication with mainframe
            """
            time.sleep(10)

    @setInterval(PROGRAM_QUEUE_CHECK_TIMER)
    def checkProgramQueue(self):
        # Check if there are messages for the program to process
        if not self._end and self.program_queue is not None:
            # This will block the program until the queue is cleared so need to avoid
            # spamming this with commands
            while not self._end and not self.program_queue.empty():
                # Use the command processor way of handling command messages
                command_message = self.program_queue.get()
                if (
                    command_message
                    and command_message.messageType == msg.MessageType.COMMAND
                ):
                    self.processCommand(
                        command_message.content, details=command_message.details
                    )

    def start(self, is_local):
        # call user funcs setup now that we are in our own process
        for uF in self._user_funcs:
            # if any of the user funcs fail to setup we'll end now
            if not uF.setup():
                mpLogging.critical(
                    "Function setup failed, function not found, program process exiting early",
                    description=f"userFunc: {uF.name}, program: {self.code}",
                    group=FUNC_GROUP,
                )
                self._end = True
                return
        # Connect to clientServerManager
        self._client_server_manager = qm.createQueueManager(is_local)
        self._client_server_manager.connect()
        assert hasattr(self._client_server_manager, qm.GET_MAINFRAME_QUEUE)
        self._mainframe_queue = getattr(
            self._client_server_manager, qm.GET_MAINFRAME_QUEUE
        )()
        self._current_mode = Modes.STARTED
        self.start_time = time.time()
        self.check_program_status_event = self.checkProgramQueue(timer=True)
        self.update_event = self._update(timer=True, on_runtime_time=self.period)
        self.keepAlive()

    def populateProgramStatusData(self, details, status_data: ProgramStatusData):
        status_data.receive_time = time.time()
        status_data.runtime = time.time() - self.start_time
        status_data.mode = self._current_mode

        if details is not None and isinstance(details, dict):
            status_data.send_time = ProgramStatusData(**details).send_time

    def sendStatusData(self, status_data: ProgramStatusData):
        returnMessage = msg.message(
            msg.MessageType.UI_UPDATE,
            msg.UiUpdateType.STATUS,
            key=msgKey.messageKey(self.code, None),
            details=asdict(status_data),
        )
        self._mainframe_queue.put(returnMessage)

    def checkStatus(self, _, details):
        """
        Aside from special cases like COLUMNS, the details on this message will be displayed on the status window
        """
        status_data = ProgramStatusData()
        self.populateProgramStatusData(details, status_data)
        self.sendStatusData(status_data)

    @setInterval(1)
    def _update(self):
        pass

    @abstractmethod
    def update(self):
        pass
