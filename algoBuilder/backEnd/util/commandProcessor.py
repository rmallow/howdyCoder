from ...core import message as msg

from ...commonUtil import mpLogging
from ...commonUtil.multiBase import multiBase

"""
used by classes that need to process commands
default commands are start, end, abort and resume
these funcs will need to be overwritten by child class
"""


class commandProcessor(multiBase):
    def __init__(self, *args, defaultCmdFunc=None, **kwargs):
        super().__init__(*args, **kwargs)
        # get copy of the dict so can make changes later
        self.cmdDict = dict(CMD_DICT)

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
        if key not in self.cmdDict or overwrite:
            self.cmdDict[key] = func
            if overwrite:
                mpLogging.warning("Overwriting command processor for key: " + str(key))

    def cmdNotFound(self, command, details=None):
        """
        @brief: default function for if command is not found

        @param: command -   command passed into command func
        """
        mpLogging.warning(
            "Command Processor command not found", description=str(command)
        )

    def cmdStart(self, command, details=None):
        """
        @brief: default function for start command, will call overwritten function in child class

        @param: command -   command passed into command func
        """
        self.cmdStart(command, details=details)

    def cmdEnd(self, command, details=None):
        """
        @brief: default function for endt command, will call overwritten function in child class

        @param: command -   command passed into command func
        """
        self.cmdEnd(command, details=details)

    def cmdAbort(self, command, details=None):
        """
        @brief: default function for abort command, will call overwritten function in child class

        @param: command -   command passed into command func
        """
        self.cmdAbort(command, details=details)

    def cmdResume(self, command, details=None):
        """
        @brief: default function for resume command, will call overwritten function in child class

        @param: command -   command passed into command func
        """
        self.cmdResume(command, details=details)

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
    msg.CommandType.START: commandProcessor.cmdStart,
    msg.CommandType.END: commandProcessor.cmdEnd,
    msg.CommandType.ABORT: commandProcessor.cmdAbort,
    msg.CommandType.RESUME: commandProcessor.cmdResume,
}
