from ..core.dataStructs import ProgramStatusData, SourceData, ProgramSettings, Modes
from .uiConstants import LOOP_INTERVAL_MSECS
from .programData import ProgramDict

from ..core.commonGlobals import RECEIVE_TIME, MAINFRAME, ProgramTypes, EditorType
from ..commonUtil import queueManager as qm
from ..commonUtil.helpers import getStrTime, getDupeName
from ..commonUtil import mpLogging, configLoader, keyringUtil

from ..core import message as msg
from ..core import messageKey
from ..backEnd.util.commandProcessor import commandProcessor
from ..core import parameterSingleton

import copy
from dataclass_wizard import asdict, fromdict
from collections import deque, Counter, defaultdict
import time
import typing

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
    updateSTDSignal = QtCore.Signal(msg.message)
    moduleStatusChangedSignal = QtCore.Signal()

    def __init__(self, isLocal: bool, parent=None):
        super().__init__(parent)
        self.ui_queue = None
        self.mainframe_queue = None
        self.client_server_manager = None
        self.incomingMessageCount = Counter()
        self.program_dict = ProgramDict()
        self.program_being_edited = None
        self._config_loader = configLoader.ConfigLoader()

        # Connect to clientServerManager
        self.client_server_manager = qm.createQueueManager(isLocal)
        self.client_server_manager.connect()

        # Get the necessary queues from the manager
        assert hasattr(self.client_server_manager, qm.GET_MAINFRAME_QUEUE)
        self.mainframe_queue = getattr(
            self.client_server_manager, qm.GET_MAINFRAME_QUEUE
        )()
        self.pending_queue = deque()
        assert hasattr(self.client_server_manager, qm.GET_UI_QUEUE)

        self.ui_queue = getattr(self.client_server_manager, qm.GET_UI_QUEUE)()
        self._module_status = {}

        self._export_mapping_cache = defaultdict(deque)

        # Send a startup command to the mainframe queue
        m = msg.message(msg.MessageType.COMMAND, msg.CommandType.UI_STARTUP)
        self.messageMainframe(m)

        """
        Add CommandProcessor Handlers, most of these will just track and emit a signal
        """
        self.addCmdFunc(msg.UiUpdateType.ALGO, mainModel.handleBlockUpdate)
        self.addCmdFunc(msg.UiUpdateType.LOGGING, mainModel.handleLoggingUpdate)
        self.addCmdFunc(msg.UiUpdateType.STATUS, mainModel.handleUIStatus)
        self.addCmdFunc(msg.UiUpdateType.STARTUP, mainModel.handleStartup)
        self.addCmdFunc(msg.UiUpdateType.CREATED, mainModel.handleCreated)
        self.addCmdFunc(msg.UiUpdateType.MOD_STATUS, mainModel.handleModStatus)
        self.addCmdFunc(msg.UiUpdateType.EXPORT, mainModel.handleExport)
        self.addCmdFunc(msg.CommandType.CHECK_UI_STATUS, mainModel.checkStatus)
        self.addCmdFunc(msg.UiUpdateType.STD_OUT_ERR, mainModel.handleSTDUpdate)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.checkQueue)
        self.timer.start(LOOP_INTERVAL_MSECS)

    @QtCore.Slot()
    def messageMainframe(self, message):
        if self.mainframe_queue:
            self.mainframe_queue.put(message)
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
            self.mainframe_queue.put(self.pending_queue.popleft())
        if self.ui_queue is not None:
            try:
                while not self.ui_queue.empty():
                    m: msg.message = self.ui_queue.get()
                    if not m.isMessageList():
                        self.processCommand(m.content, details=m)
                    else:
                        for msgIter in m.content:
                            if msgIter.content is not None:
                                self.processCommand(msgIter.content, details=msgIter)
            except (BrokenPipeError, EOFError, ConnectionResetError) as e:
                # This will happen when the server process has ended, we no longer need to keep checking
                mpLogging.error("UI Queue is disconnnected.")
                self.ui_queue = None

    def sendGlobals(self, code: str):
        globals_with_keys = {}
        for key, value in parameterSingleton.getParameters().items():
            globals_with_keys[key] = asdict(value)
            if value.type_ == EditorType.KEY.display:
                globals_with_keys[key]["value"] = keyringUtil.getKey(value.name)

        self.messageMainframe(
            msg.message(
                msg.MessageType.COMMAND,
                msg.CommandType.SET_GLOBALS,
                details=globals_with_keys,
                key=messageKey.messageKey(code, None),
            )
        )

    @QtCore.Slot()
    def sendCmdStart(self, code: str):
        if self.program_dict.getData(code).mode == Modes.STANDBY:
            self.sendGlobals(code)

        self.messageMainframe(
            msg.message(msg.MessageType.COMMAND, msg.CommandType.START, details=code)
        )

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
        data = ProgramStatusData(**details.details)
        if data.columns:
            self.updateColumnsSignal.emit(details)
        self.updateStatusSignal.emit(details)
        self.program_dict.updateProgramStatus(details.key.sourceCode, data)

    def handleBlockUpdate(self, _, details: msg.message = None):
        """
        Called by commandProcessor on UiUpdateType.ALGO
        """
        self.trackMessage(details)
        self.updateOutputSignal.emit(details)

    def handleLoggingUpdate(self, _, details: msg.message = None):
        """
        Called by commandProcessor on UiUpdateType.LOGGING
        """
        self.trackMessage(details)
        self.program_dict.updateProgramLogging(
            details.details.get(mpLogging.MP_KEY, ""), details.details
        )
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

    def addProgramFile(self, program_config_file_path: str):
        """This will only verify that the file is found, and can be turned into a dict, doesn't determine valid file"""
        if program_config_file_path:
            if config := self._config_loader.loadAndReplaceYamlFile(
                program_config_file_path
            ):
                self.addProgram(fromdict(ProgramSettings, config))

    def addProgramDict(self, program_config: typing.Dict):
        """
        Send it to the mainframe for processing
        program_config could be blank, which means we're just exiting creator
        """
        if program_config:
            self.messageMainframe(
                msg.message(
                    msg.MessageType.COMMAND,
                    msg.CommandType.CREATE,
                    program_config,
                )
            )

    @QtCore.Slot()
    def addProgramFromWizard(self, program_settings: ProgramSettings):
        if program_settings is not None and self.program_being_edited is not None:
            self.program_dict.remove(self.program_being_edited)
        self.addProgram(program_settings)

    def addProgram(self, program_settings: ProgramSettings):
        if program_settings is not None:
            if self.program_dict.contains(program_settings.name):
                program_settings.name = getDupeName(
                    program_settings.name, self.program_dict.getNames()
                )
                program_settings.settings.name = program_settings.name
            self.addProgramDict(asdict(program_settings))

    @QtCore.Slot()
    def copyProgram(self, code: str):
        if program_data := self.program_dict.getData(code):
            copied_settings = copy.deepcopy(program_data.config)
            self.addProgram(copied_settings)

    def handleCreated(self, _, details: msg.message = None):
        """Mainframe wants us to know this item was created"""
        self.trackMessage(details)
        for k, v in details.details.items():
            self.program_dict.addProgram(k, v)

    def handleModStatus(self, _, details: msg.message = None):
        """Mainframes wants us to know what modules have been found/not found"""
        self.trackMessage(details)
        self._module_status[details.details[0]] = details.details[1]
        self.moduleStatusChangedSignal.emit()

    def getModules(self, code=None):
        module_status = []
        if code is None:
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

    def shutdownProgram(self, code):
        self.messageMainframe(
            msg.message(msg.MessageType.COMMAND, msg.CommandType.SHUTDOWN, details=code)
        )

    def shutdown(self):
        self.messageMainframe(
            msg.message(msg.MessageType.COMMAND, msg.CommandType.SHUTDOWN)
        )

    def exportData(self, code, file_path):
        self._export_mapping_cache[code].append(file_path)
        self.messageMainframe(
            msg.message(
                msg.MessageType.COMMAND,
                msg.CommandType.EXPORT,
                key=msg.messageKey(code, None),
            )
        )

    def handleExport(self, _, details: msg.message = None):
        code = details.key.sourceCode
        if self._export_mapping_cache[code]:
            try:
                details.details.writeToCsv(self._export_mapping_cache[code][0])
            except AttributeError as _:
                mpLogging.error(
                    "Sparse Dict List not passed in export Ui Update message details"
                )
            else:
                self._export_mapping_cache[code].popleft()

    def inputEntered(self, input_data: SourceData):
        self.messageMainframe(
            msg.message(
                msg.MessageType.COMMAND,
                msg.CommandType.ADD_SOURCE_DATA,
                details=asdict(input_data),
                key=msg.messageKey(input_data.code, None),
            )
        )

    def handleSTDUpdate(self, _, details: msg.message = None):
        """
        Called by commandProcessor on UiUpdateType.STD_OUT_ERR
        """
        self.trackMessage(details)
        self.updateSTDSignal.emit(details)
