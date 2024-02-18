# Local common includes
from .core.dataStructs import ProgramStatusData, Modes, ProgramSettings, Parameter
from .core.commonGlobals import (
    ITEM,
    LOCAL_AUTH,
    LOCAL_PORT,
    ProgramTypes,
    EditorType,
    IMPORTS,
)

# Common Util includes
from .commonUtil import mpLogging
from .commonUtil.helpers import getStrTime
from .commonUtil import queueManager as qm
from .commonUtil.repeatTimer import setInterval

# Back End includes
from .core import message as msg
from .core import messageKey as msgKey
from .backEnd.algo import Algo
from .backEnd.script import Script
from .backEnd.program import Program
from .commonUtil import configLoader
from .backEnd.util.commandProcessor import commandProcessor

# Multi/Asyncio/Threading includes
import multiprocessing as mp

# multiprocess is Dill version of multiprocessing
import multiprocess as dill_mp

import threading

# python lib includes
import importlib
import typing
import logging
import configparser
import time
import subprocess
import sys
import traceback
from dataclasses import asdict
import dataclass_wizard
import copy

MAINFRAME_QUEUE_CHECK_TIMER = 0.3
LOGGING_QUEUE_CHECK_TIMER = 0.5
STATUS_CHECK_TIMER = 1
UI_STATUS_CHECK_TIMER = 5
UI_SEND_STATUS_CHECK = 1


class mainframe(commandProcessor):
    TYPE_TO_CONSTRUCTOR = {
        ProgramTypes.ALGO.value: Algo,
        ProgramTypes.SCRIPT.value: Script,
    }

    def __init__(self, isLocal: bool):
        """
        This is the main initializing function for all of howdyCoder except for the UI
        The mainframe is intended to be the main control center for all of the programs

        All of the separate processes are created out of the mainframe and communicate back
        with the mainframe through different queues,
        """
        super().__init__()

        self.isLocal = isLocal
        # have to set the level for logging
        logging.getLogger().setLevel(logging.INFO)

        # Load defaults
        self.loader = configLoader.ConfigLoader()

        # Set up multiprocessing items
        self.process_dict = {}
        self.statusDict = {}

        # This manager is for providing dill queues for the program processes
        self.dill_program_manager = dill_mp.Manager()

        # Set up port and auth for managers
        port = None
        authkey = None
        if not isLocal and "server.port" in self.loader.valueDict:
            port = int(self.loader.valueDict["server.port"])
        else:
            port = LOCAL_PORT
        # address is empty as the client will be acessing it
        address = ("", port)

        if not isLocal and "server.authkey" in self.loader.valueDict:
            authkey = str.encode(self.loader.valueDict["server.authkey"])
        else:
            authkey = LOCAL_AUTH

        # This manager is for cleint sessions to acess these queues
        self.client_server_manager = qm.QueueManager(address=address, authkey=authkey)

        print(
            f"Starting up server manager Address ip: {address[0]} port: {address[1]} and authkey: {authkey}"
        )
        # This queue is complicated as it's used both by local processes, that won't  be going through manager to get it
        # But it will also be used by objects that are only going to be acessing it by manager
        self.mainframe_queue = mp.Queue(-1)
        qm.QueueManager.register(
            qm.GET_MAINFRAME_QUEUE, callable=lambda: self.mainframe_queue
        )

        # This queue will only be used by mainframe and ui main model
        self.ui_queue = mp.Queue(-1)
        qm.QueueManager.register(qm.GET_UI_QUEUE, callable=lambda: self.ui_queue)

        # This queue will be accessed by all processes started with logged process
        self.logging_queue = mp.Queue(-1)
        qm.QueueManager.register(
            qm.GET_LOGGING_QUEUE, callable=lambda: self.logging_queue
        )

        # start up the manager thread for serving its objects
        self._manager_thread = threading.Thread(
            target=self.client_server_manager.get_server().serve_forever, daemon=True
        )
        self._manager_thread.start()

        # set up flag variables
        self.ui_connected = False
        self.pending_ui_messages = []
        self.ui_last_time = None

        # add commands for processor
        self.addCmdFunc(msg.CommandType.ADD_OUTPUT_VIEW, mainframe.addOutputView)
        self.addCmdFunc(msg.CommandType.UI_STARTUP, mainframe.sendStartupData)
        self.addCmdFunc(msg.CommandType.CHECK_UI_STATUS, mainframe.sendStatusCheck)
        self.addCmdFunc(msg.CommandType.CREATE, mainframe.createCommand)
        self.addCmdFunc(msg.CommandType.INSTALL_PACKAGE, mainframe.installPackages)
        self.addCmdFunc(msg.CommandType.EXPORT, mainframe.passCommandToProgram)
        self.addCmdFunc(msg.CommandType.ADD_INPUT_DATA, mainframe.passCommandToProgram)
        self.addCmdFunc(msg.CommandType.SET_GLOBALS, mainframe.setGlobals)

        # not an mp Queue, it's Dill, but we'll survive with this type hint
        self._all_program_queues: typing.Dict[str, mp.Queue] = {}
        self._all_settings_map: typing.Dict[str, ProgramSettings] = {}
        self._all_program_globals: typing.Dict[str, typing.Dict[str, Parameter]] = {}

        self.ui_status_check_event = None
        self.item_status_check_event = None

        self._is_running = True

        mpLogging.info("Finished initializing mainframe")

    def sendToUi(self, message):
        """
        If the ui queue exists and a ui is connected then send the pending ui messages
        Otherwise append to a list and send to the UI whe it does connect
        """
        if self.ui_queue is not None:
            if self.ui_connected:
                if len(self.pending_ui_messages) > 0:
                    self.sendPendingUiMessages()
                self.ui_queue.put(message)
            else:
                self.pending_ui_messages.append(message)
        else:
            mpLogging.critical(
                "Major error, ui queue is none, this should never happen"
            )

    def sendPendingUiMessages(self):
        """
        A UI has connected so send all of the pending messages in one message
        """
        mpLogging.info("Sending pending messages to the UI")
        m = msg.message(msg.MessageType.MESSAGE_LIST, self.pending_ui_messages)
        self.ui_queue.put(m)
        self.pending_ui_messages = []

    @setInterval(MAINFRAME_QUEUE_CHECK_TIMER)
    def checkMainframeQueue(self):
        """
        Check what has been sent to the mainframe to be processed
        If it's a command then process that command
        If it's for the UI then send it to the UI

        This function is run on a timer, when the function ends it will
        run the function again on a predetermined timer
        """
        while self._is_running and not self.mainframe_queue.empty():
            message = self.mainframe_queue.get()
            if isinstance(message, msg.message):
                if message.isCommand():
                    self.processCommand(message.content, details=message)
                elif message.isUIUpdate():
                    if message.content == msg.UiUpdateType.STATUS:
                        # Extra handling for status, adding back time and removing from status dict
                        # we want to do this, removing from the dict, even if uiQueue is not present
                        code = message.key.sourceCode
                        if code in self.statusDict:
                            del self.statusDict[code]
                            data = ProgramStatusData(**message.details)
                            data.back_time = getStrTime(time.time())
                            message.details = asdict(data)
                        else:
                            mpLogging.error(
                                "Trying to remove code from status dict that isn't present",
                                description=f"Code: {code}",
                            )
                            continue
                    self.sendToUi(message)

    @setInterval(LOGGING_QUEUE_CHECK_TIMER)
    def checkLoggingQueue(self):
        # Check what's in the logging queue, if the ui queue exists send to that
        while self._is_running and not self.logging_queue.empty():
            recordData = self.logging_queue.get()
            if recordData:
                uiLoggingMessage = msg.message(
                    msg.MessageType.UI_UPDATE,
                    content=msg.UiUpdateType.LOGGING,
                    details=recordData,
                )
                self.sendToUi(uiLoggingMessage)

    def sendStatusCheck(self, _1, _2=None):
        self.ui_last_time = time.time()
        if not self.ui_connected:
            # So we got a status message back after we thought the ui was disconnected, so start it back up again
            self.sendStartupData()
        # we'll just reply by sending the message back in 10 seconds
        threading.Timer(
            UI_SEND_STATUS_CHECK,
            self.sendToUi,
            [
                msg.message(
                    msg.MessageType.COMMAND, content=msg.CommandType.CHECK_UI_STATUS
                )
            ],
        )

    @setInterval(STATUS_CHECK_TIMER)
    def checkItemStatus(self):
        # Check the status of the current running programs
        for code, program_queue in self._all_program_queues.items():
            if code in self.process_dict:
                # algo process was started at one point
                if (
                    self.process_dict[code] is not None
                    and self.process_dict[code].exitcode is not None
                ):
                    # try to see if it's run its course, theres no need to wait long for it
                    # if the process is done, we'll clean it up eventually
                    self.process_dict[code].join(0.001)
                    if self.process_dict[code].is_alive():
                        del self.process_dict[code]

            if code not in self.statusDict and code in self.process_dict:
                send_time_float = time.time()
                program_queue.put(
                    msg.message(
                        msg.MessageType.COMMAND,
                        content=msg.CommandType.CHECK_STATUS,
                        details=asdict(ProgramStatusData(send_time_float)),
                    )
                )
                self.statusDict[code] = send_time_float
            elif code in self.statusDict:
                if time.time() - self.statusDict[code] > 30:
                    # program has not responded for more than 60 seconds to we're assuming it's not responsive
                    # so we'll remove it from the status dict so it's checked again
                    m = msg.message(
                        msg.MessageType.UI_UPDATE,
                        content=msg.UiUpdateType.STATUS,
                        details=asdict(
                            ProgramStatusData(
                                send_time=self.statusDict[code], mode=Modes.STANDBY
                            )
                        ),
                        key=msgKey.messageKey(code, None),
                    )
                    self.sendToUi(m)
                    del self.statusDict[code]

    def init(self):
        """
        After the mainframe object is initialized, this is the first function to be
        called when the mainframe thread starts up
        """
        self.checkMainframeQueue(timer=True)
        self.checkLoggingQueue(timer=True)
        while self._is_running:
            """Keep the non daemon thread open"""
            time.sleep(5)

    def addOutputView(self, command, details):
        if details.details[ITEM] in self._all_program_queues:
            self._all_program_queues[details.details[ITEM]].put(
                msg.message(msg.MessageType.COMMAND, command, details=details.details)
            )

    def passCommandToProgram(self, command, details):
        if details.key.sourceCode in self._all_program_queues:
            self._all_program_queues[details.key.sourceCode].put(
                msg.message(msg.MessageType.COMMAND, command, details=details.details)
            )
        else:
            mpLogging.warning(
                f"Attempted to pass command to program, but didn't find code {details.key.sourceCode}"
            )

    def sendStartupData(self, _1, _2):
        mpLogging.info("Sending startup data to the UI that was connected")
        self.ui_connected = True

        m = msg.message(msg.MessageType.UI_UPDATE, msg.UiUpdateType.STARTUP)

        # We want the startup message to be processed first so we add it to the start
        self.pending_ui_messages.insert(0, m)
        self.sendPendingUiMessages()

        # ui needs to be told about the current programs
        self.sendCreated(list(self._all_program_queues.keys()))

        # if we're not already repeatedly calling this function, then call it otherwise continue as normal
        if self.ui_status_check_event is None:
            self.ui_status_check_event = self.isUiConnected(timer=True)
        elif self.ui_status_check_event.is_set():
            self.ui_status_check_event.clear()

    @setInterval(UI_STATUS_CHECK_TIMER)
    def isUiConnected(self):
        # If the ui has responded at one point and then not for a while we're going to say it's disconnected
        # This will cause message to be sent to ui to be stored in pending messages
        # once the ui is reconnected we'll send the pending messages on one message
        # so as to not clog the queue
        if (
            self.ui_last_time
            and time.time() - self.ui_last_time > UI_STATUS_CHECK_TIMER * 3
        ):
            self.ui_connected = False
        else:
            # if we're not already repeatedly calling this function, then call it otherwise continue as normal
            if self.ui_status_check_event is None:
                self.ui_status_check_event = self.isUiConnected(timer=True)
            elif self.ui_status_check_event.is_set():
                self.ui_status_check_event.clear()

    def cmdStart(self, _, details=None):
        # run program will check if code exists, and log if not,
        # but at least check that the message details is a string
        if isinstance(details.details, str):
            self.runProgram(details.details)

    def runProgram(self, code):
        if code in self._all_settings_map:
            if code not in self.process_dict:
                self.startProgramProcess(code)
            # start the process AND then send cmd start
            if self._all_program_queues[code] is not None:
                self._all_program_queues[code].put(
                    msg.message(msg.MessageType.COMMAND, msg.CommandType.START)
                )
            else:
                mpLogging.error(
                    f"Got start message for program with a process that exists but no valid queue"
                )
        else:
            mpLogging.error(f"Error finding program with code: {code}")

        # if we're not already repeatedly calling this function, then call it otherwise continue as normal
        if self.item_status_check_event is None:
            self.item_status_check_event = self.checkItemStatus(timer=True)
        elif self.item_status_check_event.is_set():
            self.item_status_check_event.clear()

    def getGlobalSubstitutedSettings(self, code: str) -> ProgramSettings:
        settings = self._all_settings_map[code]
        global_replaced_settings = copy.deepcopy(dataclass_wizard.asdict(settings))

        def substituteGlobal(c, k, v):
            if code in self._all_program_globals:
                if "value" in c and c["value"] in self._all_program_globals[code]:
                    global_param = self._all_program_globals[code][c["value"]]
                    c["type_"] = global_param.type_
                    c["value"] = global_param.value

        configLoader.dfsConfigDict(
            global_replaced_settings,
            lambda _1, k, v: k == "type_"
            and (
                v == EditorType.GLOBAL_PARAMETER.display or v == EditorType.KEY.display,
            ),
            substituteGlobal,
        )
        return dataclass_wizard.fromdict(ProgramSettings, global_replaced_settings)

    def startProgramProcess(self, code: str):
        settings = self.getGlobalSubstitutedSettings(code)
        processName = f"{settings.type_}-" + str(code)
        program_queue = self.dill_program_manager.Queue()
        self._all_program_queues[code] = program_queue
        program_process = dill_mp.Process(
            target=mpLogging.loggedProcess,
            args=(
                self.isLocal,
                code,
                self.TYPE_TO_CONSTRUCTOR[settings.type_],
                settings,
                program_queue,
            ),
            name=processName,
            daemon=True,
        )

        self.process_dict[code] = program_process
        program_process.start()

    def cmdEnd(self, _, details=None):
        if isinstance(details.details, str):
            self.endProgram(details.details)

    def endProgram(self, code):
        if code in self.process_dict and self._all_program_queues[code] is not None:
            self._all_program_queues[code].put(
                msg.message(msg.MessageType.COMMAND, msg.CommandType.END)
            )

    def shutdownProgram(self, code, timeout=2):
        """Send the shutdown message, then try to end process nicely and then if still alive forcibly end it"""
        if code in self.process_dict:
            if self._all_program_queues[code] is not None:
                self._all_program_queues[code].put(
                    msg.message(msg.MessageType.COMMAND, msg.CommandType.SHUTDOWN)
                )
            if timeout is not None:
                self.process_dict[code].join(timeout)
            if self.process_dict[code].is_alive():
                self.process_dict[code].terminate()
            del self.process_dict[code]
        self.sendToUi(
            msg.message(
                msg.MessageType.UI_UPDATE,
                msg.UiUpdateType.STATUS,
                details=asdict(ProgramStatusData(mode=Modes.STANDBY)),
                key=msg.messageKey(code, None),
            )
        )

    def cmdShutdown(self, _, details=None):
        """End the programs first and then shutdown"""
        if details.details is None:
            self.cmdEnd(None, details)
            for k in list(self.process_dict.keys()):
                self.shutdownProgram(k)
            self._is_running = False
        elif isinstance(details.details, str):
            self.endProgram(details.details)
            self.shutdownProgram(details.details)
        else:
            mpLogging.error(
                f"Invalid details to shutdown command in mainframe: {details}"
            )

    def loadProgramSettings(self, program_settings: ProgramSettings) -> None:
        """Load the program settings but DO NOT create the program and assign queues until started"""
        self.checkModules(
            program_settings.name, dataclass_wizard.asdict(program_settings)
        )
        self._all_settings_map[program_settings.name] = program_settings

        self.sendCreated([program_settings.settings.name])

    def sendCreated(self, algo_keys_to_send: typing.List[str]):
        created_details = {}
        for key in algo_keys_to_send:
            if key in self._all_settings_map:
                created_details[key] = self._all_settings_map[key]
        if created_details:
            self.sendToUi(
                msg.message(
                    msg.MessageType.UI_UPDATE,
                    msg.UiUpdateType.CREATED,
                    details=created_details,
                )
            )

    def checkModules(self, code, config_dict):
        modules = set()
        configLoader.dfsConfigDict(
            config_dict,
            lambda _1, k, _3: k == IMPORTS,
            lambda _1, _2, v: modules.update(set(v)),
        )
        self.sendToUi(
            msg.message(
                msg.MessageType.UI_UPDATE,
                msg.UiUpdateType.MOD_STATUS,
                details=(
                    code,
                    [
                        (mod, importlib.util.find_spec(mod) is not None)
                        for mod in modules
                    ],
                ),
            )
        )

    def createCommand(self, _, details=None):
        """Wrapper for creating an algo from a command message"""
        if details.details is not None:
            program_settings = dataclass_wizard.fromdict(
                ProgramSettings, details.details
            )
            self.loadProgramSettings(program_settings)

    def installPackages(self, _, details=None):
        """Receive install pacakge command from UI, must send mod status response after"""
        if details.details is not None:
            for package in details.details:
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", package]
                    )
                except subprocess.CalledProcessError as e:
                    mpLogging.error(
                        "Exception while installing a package",
                        description=f"Package: {package}, exception: {traceback.format_exc()}",
                    )
            # now that we've installed, redo the module statuses
            for code, program_settings in self._all_settings_map.items():
                self.checkModules(code, asdict(program_settings))

    def setGlobals(self, _, details=None):
        if details.details is not None:
            for key, value in details.details.items():
                self._all_program_globals[key] = {key: dataclass_wizard.fromdict(value)}
