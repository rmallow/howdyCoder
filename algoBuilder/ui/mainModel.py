from .uiConstants import LOOP_INTERVAL_MSECS
from .algoData import AlgoDict

from ..core.commonGlobals import RECEIVE_TIME, MAINFRAME, AlgoStatusData
from ..commonUtil import queueManager as qm
from ..commonUtil.helpers import getStrTime
from ..commonUtil import mpLogging

from ..core import message as msg
from ..core import messageKey
from ..backEnd.util.commandProcessor import commandProcessor

from collections import deque, Counter
import time
import typing
import yaml
from PySide6 import QtCore

OUTPUT = "Output"
LOGGING = "Logging"
STATUS = "Status"
STARTUP = "Startup"


class mainModel(commandProcessor, QtCore.QObject):
    updateOutputSignal = QtCore.Signal(msg.message)
    updateLoggingSignal = QtCore.Signal(msg.message)
    updateStatusSignal = QtCore.Signal(msg.message)
    updateColumnsSignal = QtCore.Signal(msg.message)
    moduleStatusChangedSignal = QtCore.Signal()

    def __init__(self, isLocal: bool, parent=None):
        super().__init__(parent)
        self.uiQueue = None
        self.mainframeQueue = None
        self.clientSeverManager = None
        self.incomingMessageCount = Counter()
        self.algo_dict = AlgoDict()

        # Connect to clientServerManager
        self.clientSeverManager = qm.createQueueManager(isLocal)
        self.clientSeverManager.connect()

        # Get the necessary queues from the manager
        assert hasattr(self.clientSeverManager, qm.GET_MAINFRAME_QUEUE)
        self.mainframeQueue = getattr(self.clientSeverManager, qm.GET_MAINFRAME_QUEUE)()
        self.pending_queue = deque()
        assert hasattr(self.clientSeverManager, qm.GET_UI_QUEUE)

        self.uiQueue = getattr(self.clientSeverManager, qm.GET_UI_QUEUE)()
        self._module_status = {}

        # Send a startup command to the mainframe queue
        m = msg.message(msg.MessageType.COMMAND, msg.CommandType.UI_STARTUP)
        self.messageMainframe(m)

        """
        Add CommandProcessor Handlers, most of these will just track and emit a signal
        """
        self.addCmdFunc(msg.UiUpdateType.BLOCK, mainModel.handleBlockUpdate)
        self.addCmdFunc(msg.UiUpdateType.LOGGING, mainModel.handleLoggingUpdate)
        self.addCmdFunc(msg.UiUpdateType.STATUS, mainModel.handleUIStatus)
        self.addCmdFunc(msg.UiUpdateType.STARTUP, mainModel.handleStartup)
        self.addCmdFunc(msg.UiUpdateType.CREATED, mainModel.handleCreated)
        self.addCmdFunc(msg.UiUpdateType.MOD_STATUS, mainModel.handleModStatus)
        self.addCmdFunc(msg.CommandType.CHECK_UI_STATUS, self.checkStatus)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.checkQueue)
        self.timer.start(LOOP_INTERVAL_MSECS)

        self.testing()

    @QtCore.Slot()
    def messageMainframe(self, message):
        if self.mainframeQueue:
            self.mainframeQueue.put(message)
        else:
            # we aren't connected to the mainframe currently so add it to the pending for sending later
            self.pending_queue.append(message)

    @QtCore.Slot()
    def checkQueue(self):
        """
        Check the ui queue that this class owns
        this queue is passed in messages from the mainframe

        As this is the main event loop, check if there is anything pending to send out first
        """
        while self.pending_queue:
            self.mainframeQueue.put(self.pending_queue.popleft())
        if self.uiQueue is not None:
            try:
                while not self.uiQueue.empty():
                    m: msg.message = self.uiQueue.get()
                    if not m.isMessageList():
                        self.processCommand(m.content, details=m)
                    else:
                        for msgIter in m.content:
                            if msgIter.content is not None:
                                self.processCommand(msgIter.content, details=msgIter)
            except (BrokenPipeError, EOFError, ConnectionResetError) as e:
                # This will happen when the server process has ended, we no longer need to keep checking
                mpLogging.error("UI Queue is disconnnected.")
                self.uiQueue = None

    @QtCore.Slot()
    def sendCmdStartAll(self):
        self.messageMainframe(
            msg.message(msg.MessageType.COMMAND, msg.CommandType.START)
        )

    @QtCore.Slot()
    def sendCmdStart(self, code: str):
        self.messageMainframe(
            msg.message(msg.MessageType.COMMAND, msg.CommandType.START, details=code)
        )

    @QtCore.Slot()
    def sendCmdEndAll(self):
        self.messageMainframe(msg.message(msg.MessageType.COMMAND, msg.CommandType.END))

    @QtCore.Slot()
    def sendCmdEnd(self, code: str):
        self.messageMainframe(
            msg.message(msg.MessageType.COMMAND, msg.CommandType.END, details=code)
        )

    def trackMessage(self, message: msg.message):
        self.incomingMessageCount[message.content] += 1

        messageDetails = {RECEIVE_TIME: getStrTime(time.time())}
        messageDetails |= self.incomingMessageCount

        key = messageKey.messageKey(MAINFRAME, None)
        self.updateStatusSignal.emit(
            msg.message(
                msg.MessageType.UI_UPDATE,
                msg.UiUpdateType.STATUS,
                details=messageDetails,
                key=key,
            )
        )

    def handleUIStatus(self, _, details: msg.message = None):
        """
        If the message is status type need to do special processing
        """
        self.trackMessage(details)
        data = AlgoStatusData(**details.details)
        if data.columns:
            self.updateColumnsSignal.emit(details)
        self.updateStatusSignal.emit(details)
        self.algo_dict.updateAlgoStatus(details.key.sourceCode, data)

    def handleBlockUpdate(self, _, details: msg.message = None):
        """
        Called by commandProcessor on UiUpdateType.BLOCK
        """
        self.trackMessage(details)
        self.updateOutputSignal.emit(details)

    def handleLoggingUpdate(self, _, details: msg.message = None):
        """
        Called by commandProcessor on UiUpdateType.LOGGING
        """
        self.trackMessage(details)
        self.updateLoggingSignal.emit(details)

    def handleStartup(self, _, details: msg.message = None):
        """
        Called by commandProcessor on UiUpdateType.STARTUP
        """
        self.trackMessage(details)

    def checkStatus(self, _, details=None):
        """
        Called by commandProcessor on CommandType.CHECK_UI_STATUS
        """
        self.trackMessage(details)
        self.messageMainframe(details)

    @QtCore.Slot()
    def addAlgo(self, algo_config: typing.Dict):
        """
        Send it to the mainframe for processing
        algo_config could be blank, which means we're just exiting creator
        """
        if algo_config:
            self.messageMainframe(
                msg.message(
                    msg.MessageType.COMMAND, msg.CommandType.CREATE_ALGO, algo_config
                )
            )

    def handleCreated(self, _, details: msg.message = None):
        """Mainframe wants us to know this item was created"""
        self.trackMessage(details)
        for k, v in details.details.items():
            self.algo_dict.addAlgo(k, v)

    def handleModStatus(self, _, details: msg.message = None):
        """Mainframes wants us to know what modules have been found/not found"""
        self.trackMessage(details)
        self._module_status[details.details[0]] = details.details[1]
        self.moduleStatusChangedSignal.emit()

    def getModules(self, code=None):
        module_status = []
        if code is not None:
            module_status = set()
            for v in self._module_status.values():
                module_status.update(v)
            module_status = list(module_status)
        elif code in self._module_status:
            module_status = self._module_status[code][:]
        return module_status

    @QtCore.Slot()
    def sendInstallPackagesCommand(self, packages):
        """Receive packages to install from module dialog and send to mainframe"""
        self.messageMainframe(
            msg.message(
                msg.MessageType.COMMAND, msg.CommandType.INSTALL_PACKAGE, packages
            )
        )

    def shutdown(self):
        self.messageMainframe(
            msg.message(msg.MessageType.COMMAND, msg.CommandType.ABORT)
        )

    def testing(self):
        from ..data import datalocator

        with open(datalocator.TEST_FILE) as f:
            self.addAlgo(yaml.safe_load(f))
