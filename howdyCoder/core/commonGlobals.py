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
DATA_SET = "data_set"
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
FUNC_GROUP = "Function"


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


SCRIPT = "script"
DATA_SOURCES = "data_sources"
ACTION_LIST = "action_list"


class ProgramTypes(str, Enum):
    PROGRAM = "program"
    ALGO = "algo"
    SCRIPT = "script"


class DataSourcesTypeEnum(AdvancedEnum):
    """For indexing to work, all hides go to end"""

    _init_ = f"{ENUM_VALUE} {ENUM_DISPLAY} {ENUM_HIDE}"

    THREADED = 0, "threaded function", False
    FUNC = 1, "function", False
    STREAM = 2, "stream", False
    INPUT = 3, "Manual Input", False
    SIM = 4, "sim", True


class ActionTypeEnum(Enum):
    EVENT = "event"
    TRIGGER = "trigger"
    SCRIPT = "script"
    TEXT_MERGER = "text merger"
    CALCULATOR = "calculator"


class ActionDataType(AdvancedEnum):
    _init_ = f"{ENUM_VALUE} {ENUM_DISPLAY}"

    DATA_FRAME = 0, "pandas data frame"
    DICTIONARY_OF_LISTS = 1, "dictionary of lists"
    LISTS_OF_LISTS = 2, "lists of lists"


class InputType(Enum):
    SHORT_TEXT = "short text"
    LONG_TEXT = "long text"
    NUMBER = "number"
    MOUSE_POS = "mouse position"
    SPEECH_TO_TEXT = "speech to text"


class PathType(Enum):
    FOLDER = "Folder"
    FILE = "File"


class EditorType(AdvancedEnum):
    _init_ = f"{ENUM_VALUE} {ENUM_DISPLAY}"

    STRING = 0, "String"
    COMBO = 1, "Combo"
    INTEGER = 2, "Integer"
    DECIMAL = 3, "Decimal"
    FUNC = 4, "Function"
    FILE = 5, PathType.FILE.value
    FOLDER = 6, PathType.FOLDER.value
    GLOBAL_PARAMETER = 7, "Global Parameter"
    KEY = 8, "Key"
    ANY = 9, "any"
