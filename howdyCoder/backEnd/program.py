from .actionPool import ActionPool

from ..core.dataStructs import Modes, ProgramSettings, ProgramStatusData
from ..commonUtil.multiBase import multiBase
from ..commonUtil.userFuncCaller import UserFuncCaller
from ..core import message as msg
from ..core import messageKey as msgKey
from ..commonUtil import mpLogging
from ..commonUtil.repeatTimer import setInterval
from ..commonUtil import queueManager as qm
from ..core.commonGlobals import FUNC_GROUP, ProgramTypes
from ..core.dataStructs import USER_FUNC
from ..commonUtil import userFuncCaller
from ..commonUtil import configLoader

from ..core.commandProcessor import commandProcessor

from abc import ABC, abstractmethod
import time
import typing
from dataclasses import asdict
import threading
import multiprocessing as mp

PROGRAM_QUEUE_CHECK_TIMER = 0.5


class Program(commandProcessor, ABC):
    def __init__(
        self, is_local: bool, settings: ProgramSettings, program_queue: mp.Queue
    ):
        super().__init__()
        self.settings: ProgramSettings = settings
        self._is_local: bool = is_local

        self.action_pool: ActionPool = None
        self._end = False
        self.code = settings.name
        self._program_queue = program_queue
        self._user_funcs: typing.List[UserFuncCaller] = None
        self._mainframe_queue = None
        self.start_time: float = None
        self.period = 1
        self.type_ = ProgramTypes.PROGRAM

        self.check_program_status_event: threading.Event = None
        self.feed_update_event: threading.Event = None

        self.addCmdFunc(msg.CommandType.CHECK_STATUS, self.checkStatus)

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
        if not self._end and self._program_queue is not None:
            # This will block the program until the queue is cleared so need to avoid
            # spamming this with commands
            while not self._end and not self._program_queue.empty():
                # Use the command processor way of handling command messages

                message: msg.message = self._program_queue.get()
                if message and isinstance(message, msg.message):
                    if message.isMessageList():
                        for m in message.content:
                            self.processMessage(m)
                    else:
                        self.processMessage(message)

    def processMessage(self, message: msg.message):
        if message and message.isCommand():
            self.processCommand(message)

    def start(self):
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
        self._client_server_manager = qm.createQueueManager(self._is_local)
        self._client_server_manager.connect()
        assert hasattr(self._client_server_manager, qm.GET_MAINFRAME_QUEUE)
        self._mainframe_queue = getattr(
            self._client_server_manager, qm.GET_MAINFRAME_QUEUE
        )()
        self.start_time = time.time()
        self._run_time: int = 0
        self._last_status: int = None
        self.check_program_status_event = self.checkProgramQueue(timer=True)
        self.update_event = self._update(timer=True, on_runtime_time=self.period)
        self.keepAlive()

    def populateProgramStatusData(self, details, status_data: ProgramStatusData):
        if self.getMode() == Modes.RUNNING and self._last_status is not None:
            self._run_time += time.time() - self._last_status
        self._last_status = time.time()
        status_data.receive_time = time.time()
        status_data.runtime = self._run_time
        status_data.mode = self.getMode()

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

    def getStatusDataInstance(self):
        return ProgramStatusData()

    def populateTypeSpecificStatusData(self, details, status_data):
        pass

    def checkStatus(self, command_message: msg.message):
        """
        Aside from special cases like COLUMNS, the details on this message will be displayed on the status window
        """
        status_data = self.getStatusDataInstance()
        self.populateProgramStatusData(command_message.details, status_data)
        self.populateTypeSpecificStatusData(command_message.details, status_data)
        self.sendStatusData(status_data)

    @setInterval(1)
    def _update(self):
        if self.getMode() == Modes.RUNNING:
            self.update()

    @abstractmethod
    def update(self):
        pass

    def onRunning(self, old_mode: Modes):
        self.action_pool.started()

    def onStandby(self, command, details=None):
        self._end = True

    def doActions(self):
        data_list = self.action_pool.doActions()
        if data_list:
            self._mainframe_queue.put(
                msg.message(
                    msg.MessageType.UI_UPDATE,
                    msg.UiUpdateType.STD_OUT_ERR,
                    key=msgKey.messageKey(self.code, None),
                    details=[asdict(d) for d in data_list],
                )
            )

    def addUserFuncs(self, config: typing.Dict[str, typing.Any]):
        user_funcs = []

        def assignUserFuncCaller(c, k, v):
            nonlocal user_funcs
            if c is not None:
                user_funcs.append(userFuncCaller.UserFuncCaller(**c))
                c[k] = user_funcs[-1]

        configLoader.dfsConfigDict(
            config, lambda _1, k, _3: k == USER_FUNC, assignUserFuncCaller
        )
        return user_funcs
