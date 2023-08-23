from enum import Enum
from dataclasses import dataclass, field
import typing

# Dict Keys
BLOCK = "block"
HANDLER = "handler"
TYPE = "type"
ITEM = "item"
KEY = "key"
BACKTRACK = "backtrack"
GRAPH_SETTINGS = "graph settings"
PERIOD = "period"
RECEIVE_TIME = "receive time"
FIRST = "first"
DATA_SET = "dataSet"
PASSBACK_DICT = "passback_dict"

NOT_AVAIL_STR = "N/A"
MAINFRAME = "Mainframe"

# Logging groups
ACTION_GROUP = "Action"
BLOCK_GROUP = "Block"
FEED_GROUP = "Feed"
HANDLER_GROUP = "Handler"
ROUTER_GROUP = "Router"
UI_GROUP = "UI"
DATA_GROUP = "Data"
FUNC_GROUP = "Func"


# aenum ENUM constants
ENUM_VALUE = "value"
ENUM_DISPLAY = "display"
ENUM_HIDE = "hide"
ENUM_TYPE = "type"
ENUM_EDITOR_VALUES = "editorValues"
ENUM_ENABLED = "enabled"

LOCAL_AUTH = b"abcAuth"
LOCAL_PORT = 50000


class Modes(str, Enum):
    NONE = ""
    STANDBY = "Standby"
    STARTED = "Started"
    STOPPED = "Stopped"


@dataclass
class AlgoStatusData:
    send_time: float = 0.0
    receive_time: float = 0.0
    data_length: int = 0
    feed_last_update_time: float = 0.0
    runtime: float = 0.0
    columns: list = field(default_factory=list)
    mode: Modes = Modes.STANDBY
    back_time: float = 0.0


@dataclass
class InputData:
    code: str = ""
    data_source_name: str = ""
    val: typing.Any = None
