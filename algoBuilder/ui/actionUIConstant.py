from ..core.commonGlobals import ENUM_VALUE, ENUM_DISPLAY
from ..core.configConstants import (
    FUNC_NAME,
    FUNC_LOCAITON,
    FUNC_CODE,
    IMPORTS,
    IMPORT_STATEMENTS,
)

from aenum import Enum

INVALID_ACTION_KEY = "__INVALID_ACTION__"


class ActionEnum(Enum):

    _init_ = f"{ENUM_VALUE} {ENUM_DISPLAY}"

    NAME = 0, "Name"
    TYPE = 1, "Type"
    ACTION_FUNC = 2, "Function"
    INPUT = 3, "Input"
    AGGREGATE = 4, "Aggregate"
    PERIOD = 5, "Period"
    DISPLAY_ROWS = 6, ""
    PARAMETER = 7, ""
    TRIGGER_TYPE = 8, ""
    OUTPUT_FUNC = 9, ""


class ActionFuncEnum(Enum):
    _init_ = f"{ENUM_VALUE} {ENUM_DISPLAY}"

    LOCATION = 0, FUNC_LOCAITON
    NAME = 1, FUNC_NAME
    CODE = 2, FUNC_CODE
    IMPORTS = 3, IMPORTS
    IMPORT_STATEMENTS = 4, IMPORT_STATEMENTS
    INDEX = 5, ""


class DataSetEnum(Enum):
    _init_ = f"{ENUM_VALUE} {ENUM_DISPLAY}"

    INDEX = 0, "Index"
    SOURCE = 1, "Source"
    MAPPING = 2, "Mapping"


class TriggerTypeEnum(Enum):
    _init_ = f"{ENUM_VALUE} {ENUM_DISPLAY}"

    MESSAGE = 0, "Message"
    FUNCTION = 1, "Function"


class AggregateTypeEnum(Enum):
    _init_ = f"{ENUM_VALUE} {ENUM_DISPLAY}"

    NONE = 0, "None"
    PARAMETER = 1, "Parameter"
    DATA = 2, "Data"
    PARAMETER_DATA = 3, "Parameter Data"
