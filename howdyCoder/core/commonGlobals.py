from enum import Enum
from aenum import Enum as AdvancedEnum


# Dict Keys=
HANDLER = "handler"
TYPE = "type"
ITEM = "item"
KEY = "key"
LABEL = "label"
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
ALGO_GROUP = "Algo"
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


"""Constants for fields used in configuraiton files"""
FUNC_LOCAITON = "location"
FUNC_NAME = "name"
FUNC_CODE = "code"
IMPORTS = "imports"
IMPORT_STATEMENTS = "import_statements"
MAPPING = "mapping"


NONE_GROUP = "None"
SCRIPT = "script"
DATA_SOURCES = "data_sources"
ACTION_LIST = "action_list"

GROUP_SET = set([NONE_GROUP, DATA_SOURCES, ACTION_LIST, SCRIPT])


class ProgramTypes(str, Enum):
    PROGRAM = "program"
    ALGO = "algo"
    SCRIPT = "script"


class DataSourcesTypeEnum(AdvancedEnum):
    """For indexing to work, all hides go to end"""

    _init_ = f"{ENUM_VALUE} {ENUM_DISPLAY} {ENUM_HIDE}"

    THREADED = 0, "threaded", False
    FUNC = 1, "func", False
    STREAM = 2, "stream", False
    INPUT = 3, "input", False
    SIM = 4, "sim", True


class ActionTypeEnum(AdvancedEnum):
    _init_ = f"{ENUM_VALUE} {ENUM_DISPLAY}"

    EVENT = 0, "event"
    TRIGGER = 1, "trigger"


class ActionDataType(AdvancedEnum):
    _init_ = f"{ENUM_VALUE} {ENUM_DISPLAY}"

    DATA_FRAME = 0, "pandas data frame"
    DICTIONARY_OF_LISTS = 1, "dictionary of lists"
    LISTS_OF_LISTS = 2, "lists of lists"


class InputType(Enum):
    SHORT_TEXT = "short text"
    LONG_TEXT = "long text"
    NUMBER = "number"
