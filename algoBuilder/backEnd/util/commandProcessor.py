from ...core import message as msg
from ...core.commonGlobals import Modes

from ...commonUtil import mpLogging
from ...commonUtil.multiBase import multiBase

"""
used by classes that need to process commands
default commands are start, end, shutdown
these funcs will need to be overwritten by child class
"""


class commandProcessor(multiBase):
    def __init__(self, *args, defaultCmdFunc=None, **kwargs):
        super().__init__(*args, **kwargs)
        # get copy of the dict so can make changes later
        self.cmdDict = dict(CMD_DICT)
        self._current_mode = Modes.STANDBY

        # set default command function for unrecognized commands
        if defaultCmdFunc is not None:
            self.defaultCmdFunc = defaultCmdFunc
        else:
            self.defaultCmdFunc = commandProcessor.cmdNotFound

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

    def cmdNotFound(self, command, details=None):
        """
        @brief: default function for if command is not found

        @param: command -   command passed into command func
        """
        mpLogging.warning(
            "Command Processor command not found", description=str(command)
        )

    def cmdStart(self, command, details=None):
        """overwritten in child for special instructions"""
        pass

    def _cmdStart(self, command, details=None):
        """intro for command, handles mode"""
        self._current_mode = Modes.STARTED
        self.cmdStart(command, details=details)

    def cmdEnd(self, command, details=None):
        """overwritten in child for special instructions"""
        pass

    def _cmdEnd(self, command, details=None):
        """intro for command, handles mode"""
        self._current_mode = Modes.STOPPED
        self.cmdEnd(command, details=details)

    def cmdShutdown(self, command, details=None):
        """overwritten in child for special instructions"""
        pass

    def _cmdShutdown(self, command, details=None):
        """intro for command, handles mode"""
        self._current_mode = Modes.STANDBY
        self.cmdShutdown(command, details=details)

    def processCommand(self, command, details=None):
        """
        @brief: main command processor, calls function based on command value or default func

        @param: command         -  command passed into command func
                    command determines what func to call
        @param: details (None)  - extra details for command processing
        """
        if details is None:
            self.cmdDict.get(command, commandProcessor.cmdNotFound)(self, command)
        else:
            self.cmdDict.get(command, commandProcessor.cmdNotFound)(
                self, command, details
            )


"""
Default command dict, copied on commandProcessor initalization
"""
CMD_DICT = {
    msg.CommandType.START: commandProcessor._cmdStart,
    msg.CommandType.END: commandProcessor._cmdEnd,
    msg.CommandType.SHUTDOWN: commandProcessor._cmdShutdown,
}
