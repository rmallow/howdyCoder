from enum import Enum, auto, IntEnum
from dataclasses import dataclass
from .messageKey import messageKey

import typing


class MessageType(IntEnum):
    COMMAND = auto()
    NORMAL = auto()
    PRIORITY = auto()
    UI_UPDATE = auto()
    MESSAGE_LIST = auto()


class CommandType(IntEnum):
    # general commands
    START = max(e.value for e in MessageType) + 1
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
    ADD_INPUT_DATA = auto()


class UiUpdateType(IntEnum):
    OUTPUT = max(e.value for e in CommandType) + 1
    BLOCK = auto()
    HANDLER = auto()
    LOGGING = auto()
    STATUS = auto()
    STARTUP = auto()
    CREATED = auto()
    MOD_STATUS = auto()
    EXPORT = auto()


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
