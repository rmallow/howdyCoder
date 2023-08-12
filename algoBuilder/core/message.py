from enum import Enum, auto, IntEnum
from dataclasses import dataclass
from .messageKey import messageKey

import typing


class MessageType(Enum):
    COMMAND = 1
    NORMAL = 2
    PRIORITY = 3
    UI_UPDATE = 4
    MESSAGE_LIST = 5


class CommandType(IntEnum):
    # general commands
    START = auto()
    END = auto()
    SHUTDOWN = auto()
    CLEAR = auto()
    # specific use case commands
    ADD_OUTPUT_VIEW = auto()
    CHECK_STATUS = auto()
    CHECK_UI_STATUS = auto()
    UI_STARTUP = auto()
    CREATE_ALGO = auto()
    CHECK_MODULES = auto()
    INSTALL_PACKAGE = auto()
    EXPORT = auto()


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
