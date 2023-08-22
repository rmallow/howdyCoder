# Local common includes
from .data.datalocator import SETTINGS_FILE
from .core.commonGlobals import (
    ITEM,
    LOCAL_AUTH,
    LOCAL_PORT,
    AlgoStatusData,
    Modes,
)
from .core.configConstants import IMPORTS

# Common Util includes
from .commonUtil import mpLogging
from .commonUtil.helpers import getStrTime
from .commonUtil import queueManager as qm
from .commonUtil.repeatTimer import setInterval

# Back End includes
from .core import message as msg
from .core import messageKey as msgKey
from .backEnd.algoManager import AlgoManager
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

MAINFRAME_QUEUE_CHECK_TIMER = 0.3
LOGGING_QUEUE_CHECK_TIMER = 0.5
STATUS_CHECK_TIMER = 1
UI_STATUS_CHECK_TIMER = 5
UI_SEND_STATUS_CHECK = 1


class mainframe(commandProcessor):
    def __init__(self, isLocal: bool):
        """
        This is the main initializing function for all of howdyCoder except for the UI
        The mainframe is intended to be the main control center for all of the blocks
        and the message router / handlers

        All of the separate processes are created out of the mainframe and communicate back
        with the mainframe through different queues,
        """
        super().__init__()

        self.isLocal = isLocal
        # have to set the level for logging
        logging.getLogger().setLevel(logging.INFO)

        # Set up item managers, unrelated to multiprocessing managers
        self.algo_manager = None

        # Load defaults
        self.loader = configLoader.ConfigLoader(SETTINGS_FILE)

        # Set up multiprocessing items
        self.process_dict = {}
        self.statusDict = {}

        # This manager is for providing dill queues for the block processes
        self.dill_algo_manager = dill_mp.Manager()

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
        self.clientSeverManager = qm.QueueManager(address=address, authkey=authkey)

        print(
            f"Starting up server manager Address ip: {address[0]} port: {address[1]} and authkey: {authkey}"
        )
        # This queue is complicated as it's used both by local processes, that won't  be going through manager to get it
        # But it will also be used by objects that are only going to be acessing it by manager
        self.mainframeQueue = mp.Queue(-1)
        qm.QueueManager.register(
            qm.GET_MAINFRAME_QUEUE, callable=lambda: self.mainframeQueue
        )

        # This queue will only be used by mainframe and ui main model
        self.uiQueue = mp.Queue(-1)
        qm.QueueManager.register(qm.GET_UI_QUEUE, callable=lambda: self.uiQueue)

        # This queue will be accessed by all processes started with logged process
        self.loggingQueue = mp.Queue(-1)
        qm.QueueManager.register(
            qm.GET_LOGGING_QUEUE, callable=lambda: self.loggingQueue
        )

        # start up the manager thread for serving its objects
        self._manager_thread = threading.Thread(
            target=self.clientSeverManager.get_server().serve_forever, daemon=True
        )
        self._manager_thread.start()

        # set up flag variables
        self.uiConnected = False
        self.pendingUiMessages = []
        self.uiLastTime = None

        # add commands for processor
        self.addCmdFunc(msg.CommandType.ADD_OUTPUT_VIEW, mainframe.addOutputView)
        self.addCmdFunc(msg.CommandType.UI_STARTUP, mainframe.sendStartupData)
        self.addCmdFunc(msg.CommandType.CHECK_UI_STATUS, mainframe.sendStatusCheck)
        self.addCmdFunc(msg.CommandType.CREATE_ALGO, mainframe.createAlgoCommand)
        self.addCmdFunc(msg.CommandType.INSTALL_PACKAGE, mainframe.installPackages)
        self.addCmdFunc(msg.CommandType.EXPORT, mainframe.passCommandToBlock)

        # Get other config files to load
        config = configparser.ConfigParser()
        config.read(SETTINGS_FILE)

        # init block manager
        self.algo_manager = AlgoManager()

        self.ui_status_check_event = None
        self.item_status_check_event = None

        self._is_running = True

        mpLogging.info("Finished initializing mainframe")

    def sendToUi(self, message):
        """
        If the ui queue exists and a ui is connected then send the pending ui messages
        Otherwise append to a list and send to the UI whe it does connect
        """
        if self.uiQueue is not None:
            if self.uiConnected:
                if len(self.pendingUiMessages) > 0:
                    self.sendPendingUiMessages()
                self.uiQueue.put(message)
            else:
                self.pendingUiMessages.append(message)
        else:
            mpLogging.critical(
                "Major error, ui queue is none, this should never happen"
            )

    def sendPendingUiMessages(self):
        """
        A UI has connected so send all of the pending messages in one message
        """
        mpLogging.info("Sending pending messages to the UI")
        m = msg.message(msg.MessageType.MESSAGE_LIST, self.pendingUiMessages)
        self.uiQueue.put(m)
        self.pendingUiMessages = []

    @setInterval(MAINFRAME_QUEUE_CHECK_TIMER)
    def checkMainframeQueue(self):
        """
        Check what has been sent to the mainframe to be processed
        If it's a command then process that command
        If it's for the UI then send it to the UI

        This function is run on a timer, when the function ends it will
        run the function again on a predetermined timer
        """
        while self._is_running and not self.mainframeQueue.empty():
            message = self.mainframeQueue.get()
            if isinstance(message, msg.message):
                if message.isCommand():
                    self.processCommand(message.content, details=message.details)
                elif message.isUIUpdate():
                    if message.content == msg.UiUpdateType.STATUS:
                        # Extra handling for status, adding back time and removing from status dict
                        # we want to do this, removing from the dict, even if uiQueue is not present
                        code = message.key.sourceCode
                        if code in self.statusDict:
                            del self.statusDict[code]
                            data = AlgoStatusData(**message.details)
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
        while self._is_running and not self.loggingQueue.empty():
            recordData = self.loggingQueue.get()
            if recordData:
                uiLoggingMessage = msg.message(
                    msg.MessageType.UI_UPDATE,
                    content=msg.UiUpdateType.LOGGING,
                    details=recordData,
                )
                self.sendToUi(uiLoggingMessage)

    def sendStatusCheck(self, content, details=None):
        self.uiLastTime = time.time()
        if not self.uiConnected:
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
        # Check the status of the current running blocks
        for code, block in self.algo_manager.blocks.items():
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
                block.block_queue.put(
                    msg.message(
                        msg.MessageType.COMMAND,
                        content=msg.CommandType.CHECK_STATUS,
                        details=asdict(AlgoStatusData(send_time_float)),
                    )
                )
                self.statusDict[code] = send_time_float
            elif code in self.statusDict:
                if time.time() - self.statusDict[code] > 30:
                    # block has not responded for more than 60 seconds to we're assuming it's not responsive
                    # so we'll remove it from the status dict so it's checked again
                    m = msg.message(
                        msg.MessageType.UI_UPDATE,
                        content=msg.UiUpdateType.STATUS,
                        details=asdict(
                            AlgoStatusData(
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
        if details[ITEM] in self.algo_manager.blocks:
            block = self.algo_manager.blocks[details[ITEM]]
            block.block_queue.put(
                msg.message(msg.MessageType.COMMAND, command, details=details)
            )

    def passCommandToBlock(self, command, details):
        if details in self.algo_manager.blocks:
            self.algo_manager.blocks[details].block_queue.put(
                msg.message(msg.MessageType.COMMAND, command, details=details)
            )
        else:
            mpLogging.warning(
                f"Attempted to pass command to block, but didn't find code {details}"
            )

    def sendStartupData(self, _):
        mpLogging.info("Sending startup data to the UI that was connected")
        self.uiConnected = True

        m = msg.message(msg.MessageType.UI_UPDATE, msg.UiUpdateType.STARTUP)

        # We want the startup message to be processed first so we add it to the start
        self.pendingUiMessages.insert(0, m)
        self.sendPendingUiMessages()

        # ui needs to be told about the current blocks and handlers
        self.sendCreated(self.algo_manager.blocks.keys())

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
            self.uiLastTime
            and time.time() - self.uiLastTime > UI_STATUS_CHECK_TIMER * 3
        ):
            self.uiConnected = False
        else:
            # if we're not already repeatedly calling this function, then call it otherwise continue as normal
            if self.ui_status_check_event is None:
                self.ui_status_check_event = self.isUiConnected(timer=True)
            elif self.ui_status_check_event.is_set():
                self.ui_status_check_event.clear()

    def cmdStart(self, _, details=None):
        # Called by command processor on receiving the start command message
        if details is None:
            for code, _ in self.algo_manager.blocks.items():
                self.runBlock(code)
        else:
            # run block will check if code exists, and log if not,
            # but at least check that the message details is a string
            if isinstance(details, str):
                self.runBlock(details)

    def runBlock(self, code):
        if code in self.algo_manager.blocks:
            if code not in self.process_dict:
                block = self.algo_manager.blocks[code]
                self.startBlockProcess(code, block)
            elif self.algo_manager.blocks[code].block_queue is not None:
                self.algo_manager.blocks[code].block_queue.put(
                    msg.message(msg.MessageType.COMMAND, msg.CommandType.START)
                )
            else:
                mpLogging.error(
                    f"Got start message for block with a process that exists but no valid queue"
                )
        else:
            mpLogging.error(f"Error finding block with code: {code}")

        # if we're not already repeatedly calling this function, then call it otherwise continue as normal
        if self.item_status_check_event is None:
            self.item_status_check_event = self.checkItemStatus(timer=True)
        elif self.item_status_check_event.is_set():
            self.item_status_check_event.clear()

    def startBlockProcess(self, code, block):
        processName = "Block-" + str(code)
        blockProcess = dill_mp.Process(
            target=mpLogging.loggedProcess,
            args=(self.isLocal, code, block.start),
            name=processName,
            daemon=True,
        )

        self.process_dict[code] = blockProcess
        blockProcess.start()

    def cmdEnd(self, _, details=None):
        # Called by command processor on receiving the end command message
        if details is None:
            for k in list(self.process_dict.keys()):
                self.endBlock(k)
        else:
            if isinstance(details, str):
                self.endBlock(details)

    def endBlock(self, code):
        if (
            code in self.process_dict
            and self.algo_manager.blocks[code].block_queue is not None
        ):
            self.algo_manager.blocks[code].block_queue.put(
                msg.message(msg.MessageType.COMMAND, msg.CommandType.END)
            )

    def shutdownBlock(self, code, timeout=2):
        """Send the shutdown message, then try to end process nicely and then if still alive forcibly end it"""
        if code in self.process_dict:
            if self.algo_manager.blocks[code].block_queue is not None:
                self.algo_manager.blocks[code].block_queue.put(
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
                    details=asdict(AlgoStatusData(mode=Modes.STANDBY)),
                    key=msg.messageKey(code, None),
                )
            )

    def cmdShutdown(self, _, details=None):
        """End the blocks first and then shutdown"""
        if details is None:
            self.cmdEnd(None)
            for k in list(self.process_dict.keys()):
                self.shutdownBlock(k)
            self._is_running = False
        elif isinstance(details, str):
            self.endBlock(details)
            self.shutdownBlock(details)
        else:
            mpLogging.error(
                f"Invalid details to shutdown command in mainframe: {details}"
            )

    def loadAlgoConfigFile(self, config: str):
        """Load an algo based on a config file"""
        if config:
            config_dict = self.loader.loadAndReplaceYamlFile(config)
            self.loadAlgos(config_dict)

    def loadAlgos(self, config_dict: typing.Dict[str, typing.Any]) -> None:
        """Load the algos and assign the queues they need for mainframe communication"""
        self.checkModules(config_dict)
        for algo in self.algo_manager.loadBlocks(config_dict):
            algo.block_queue = self.dill_algo_manager.Queue()

        self.sendCreated(config_dict.keys())

    def sendCreated(self, algo_keys_to_send: typing.List[str]):
        created_details = {}
        for key in algo_keys_to_send:
            if key in self.algo_manager.blocks:
                created_details[key] = self.algo_manager.blocks[key].config
        if created_details:
            self.sendToUi(
                msg.message(
                    msg.MessageType.UI_UPDATE,
                    msg.UiUpdateType.CREATED,
                    details=created_details,
                )
            )

    def checkModules(self, config_dict):
        for code, config in config_dict.items():
            modules = set()
            configLoader.dfsConfigDict(
                config, lambda k: k == IMPORTS, lambda _1, _2, v: modules.update(set(v))
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

    def createAlgoCommand(self, _, details=None):
        """Wrapper for creating an algo from a command message"""
        if details is not None:
            self.loadAlgos(details)

    def installPackages(self, _, details=None):
        """Receive install pacakge command from UI, must send mod status response after"""
        if details is not None:
            for package in details:
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
            for code, algo in self.algo_manager.blocks.items():
                self.checkModules({code: algo.config})
