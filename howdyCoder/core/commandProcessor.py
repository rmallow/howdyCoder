from . import message as msg
from .modeHandler import ModeHandler
from .dataStructs import Modes

from ..commonUtil import mpLogging
from ..commonUtil.multiBase import multiBase

from collections import defaultdict

"""
used by classes that need to process commands
default commands are start, end, shutdown
these funcs will need to be overwritten by child class
"""


class commandProcessor(ModeHandler):
    def __init__(self, *args, default_cmd_func=None, **kwargs):
        super().__init__(*args, **kwargs)
        # get copy of the dict so can make changes later
        self.cmdDict = {
            msg.CommandType.CHANGE_MODE: self.cmdChangeMode,
            msg.CommandType.SEND_COMMAND_TO_CHILD: self.sendCommandToChild,
        }

        self._batch_process_messages = False
        self._message_list_batch = defaultdict(list)

        # set default command function for unrecognized commands
        if default_cmd_func is not None:
            self.default_cmd_func = default_cmd_func
        else:
            self.default_cmd_func = commandProcessor.cmdNotFound

    def removeCmdFunc(self, key):
        """
        @brief: remove command function from command func dict, no longer makes it callable

        @param: key in cmd dict to remove
        """
        self.cmdDict.pop(key, None)

    def addCmdFunc(self, key, func, overwrite=False):
        """
        @brief: add command function from command func dict, no longer makes it callable

        @param: key -   key in cmd dict to add
        @param: func -  to add at key
            rather than passing in self.xyz must pass in className.xyz
        @param: overwrite - bool, whether to overwrite if key already exists
        """
        if not overwrite:
            assert key not in self.cmdDict, "Conflicting command key value"
        elif key in self.cmdDict:
            mpLogging.warning("Overwriting command processor for key: " + str(key))
        self.cmdDict[key] = func

    def cmdNotFound(self, command_message: msg.message):
        """
        @brief: default function for if command is not found

        @param: command_message -   command passed into command func
        """
        mpLogging.warning(
            "Command Processor command not found",
            description=str(command_message.content),
        )

    def cmdChangeMode(self, command_message: msg.message):
        """Changes mode using underlying class based on mode in details"""
        self.changeMode(command_message.details)

    def getChildPutFunc(self, code: str):
        """Functionality overriden in child"""
        return None

    def sendCommandToChild(self, command_message: msg.message):
        put_func = self.getChildPutFunc(command_message.key.sourceCode)
        if put_func is not None:
            pass_through_message = command_message.details
            if self._batch_process_messages:
                self._message_list_batch[command_message.key.sourceCode].append(
                    pass_through_message
                )
            else:
                put_func(pass_through_message)
        else:
            mpLogging.warning(
                f"Attempted to pass command to child, but didn't find a put func for message with code {command_message.key.sourceCode}"
            )

    def startBatch(self):
        """Start a batch to be processed at the end"""
        self._batch_process_messages = True
        self._message_list_batch.clear()

    def processBatch(self):
        for code, message_list in self._message_list_batch.items():
            put_func = self.getChildPutFunc(code)
            if put_func is not None:
                put_func(msg.message(msg.MessageType.MESSAGE_LIST, message_list))
        self._message_list_batch.clear()
        self._batch_process_messages = False

    def processCommand(self, command_message: msg.message):
        """
        @brief: main command processor, calls function based on command value or default func

        @param: command         -  command passed into command func
                    command determines what func to call
        """
        self.cmdDict.get(command_message.content, self.cmdNotFound)(command_message)
