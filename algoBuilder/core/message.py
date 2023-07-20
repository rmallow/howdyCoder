from enum import Enum
from dataclasses import dataclass
from .messageKey import messageKey

import typing


class MessageType(Enum):
    COMMAND = 1
    NORMAL = 2
    PRIORITY = 3
    UI_UPDATE = 4
    MESSAGE_LIST = 5


class CommandType(Enum):
    # general commands
    START = 1
    END = 2
    ABORT = 3
    RESUME = 4
    CLEAR = 5
    # specific use case commands
    ADD_OUTPUT_VIEW = 6
    CHECK_STATUS = 7
    CHECK_UI_STATUS = 8
    UI_STARTUP = 9
    CREATE_ALGO = 10
    CHECK_MODULES = 11
    INSTALL_PACKAGE = 12


class UiUpdateType(Enum):
    OUTPUT = 1
    BLOCK = 2
    HANDLER = 3
    LOGGING = 4
    STATUS = 5
    STARTUP = 6
    CREATED = 7
    MOD_STATUS = 8


"""
Message type - determines what to do with message
Content - main part of message, such as command type or data
Details - extra supporting parts to message, stored outside content and not required
name    - name of message
sourceName  - name of source that sent message
key     - code and time of message
"""


@dataclass
class message:
    messageType: MessageType
    content: typing.Any
    details: typing.Any = None
    name: str = ""
    sourceName: str = ""
    key: messageKey = messageKey(None, None)
    """
    key - key of where the message originated from
    """

    def keyExists(self):
        return self.key.sourceCode is not None and self.key.time is not None

    def isPriority(self):
        return self.messageType == MessageType.PRIORITY

    def isCommand(self):
        return self.messageType == MessageType.COMMAND

    def isNormal(self):
        return self.messageType == MessageType.NORMAL

    def isUIUpdate(self):
        return self.messageType == MessageType.UI_UPDATE

    def isMessageList(self):
        return self.messageType == MessageType.MESSAGE_LIST
