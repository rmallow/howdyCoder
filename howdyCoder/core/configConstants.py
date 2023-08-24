from .commonGlobals import ENUM_VALUE, ENUM_DISPLAY, ENUM_HIDE

from aenum import Enum as AdvancedEnum
from enum import Enum

"""Constants for fields used in configuraiton files"""
NAME = "name"
EXPORT = "export"
CSV = "csv"
TYPE = "type"
DATA_TYPE = "dataType"
TYPE_SPECIFIC = "typeSpecific"
DATA_SOURCES = "dataSources"
PARAMETERS = "parameters"
SETUP_FUNCS = "setupFuncs"
SEQUENTIAL = "sequential"
PERIOD = "period"
SINGLE_SHOT = "single_shot"
FLATTEN = "flatten"
GET_FUNC = "getFunc"
ACTION_LIST = "actionList"
CALC_FUNC = "calcFunc"
OUTPUT_FUNC = "output_func"
INPUT = "input_data"  # not using input as it is a reserved keyword
REQUIRES_NEW = "requires_new"
OUTPUT = "output"
AGGREGATE = "aggregate"
INPUT_TYPE = "input_type"

FUNC_LOCAITON = "location"
FUNC_NAME = "name"
FUNC_CODE = "code"
IMPORTS = "imports"
IMPORT_STATEMENTS = "import_statements"
MAPPING = "mapping"
ACTION_DATA_TYPE = "action_data_type"

"""Data Stream Config"""
KEY = "key"
LABEL = "label"


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
