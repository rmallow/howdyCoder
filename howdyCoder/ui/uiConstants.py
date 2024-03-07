from enum import Enum, auto

from PySide6.QtGui import QColorConstants

LOOP_INTERVAL_MSECS = 300
GUI_REFRESH_INTERVAL = 500


class CreateWizardItemType(str, Enum):
    SCRIPT = "script"
    ACTION = "action"
    DATA_SOURCE = "data_source"


class outputTypesEnum(Enum):
    TABLE = "Table"
    GRAPH = "Graph"
    PRINTED = "Printed"


class InputTypesEnum(Enum):
    SHORT_TEXT = "Short Text"
    LONG_TEXT = "Long Text"
    NUMBER = "Number"


GRAPH_TYPES = ["line", "bar"]
GRAPH_COLORS = [
    "blue",
    "orange",
    "green",
    "red",
    "purple",
    "brown",
    "pink",
    "gray",
    "olive",
    "cyan",
]


class PageKeys(Enum):
    NO_PAGE = "None"
    NAME = "Name"
    PARAMETERS = "Parameters"
    SETTINGS = "Settings"
    CONFRIM = "Confirm"
    ADD_ACTION = "Add Action"
    ACTION_TYPE = "Action Type"
    ACTION = "Action"
    ADD_DATA_SOURCE = "Add Data Source"
    DATA_SOURCE_TYPE = "Data Source Type"
    DATA_SOURCE = "Data Source"
    SCRIPT = "Script"
    FINAL_CONFIRM = "Final Confirm"


class SceneMode(Enum):
    ACTION = auto()
    TOPO_VIEW = auto()


PROGRESS_BAR_HEIGHT = 10

PROGRESS_BAR_UNCOMPLETED_COLOR_STR = "#808080"
PROGRESS_BAR_UNCOMPLETED_COLOR = QColorConstants.DarkGray
PROGRESS_BAR_CURRENT_COLOR_STR = "#0000ff"
PROGRESS_BAR_CURRENT_COLOR = QColorConstants.Blue
PROGRESS_BAR_COMPLETED_COLOR_STR = "#00ff00"
PROGRESS_BAR_COMPLETED_COLOR = QColorConstants.Green
PROGRESS_BAR_FAILED_COLOR_STR = "#ff0000"
PROGRESS_BAR_FAILED_COLOR = QColorConstants.Red


class LaunchSequenceSteps(Enum):
    CHECK_GLOBALS = 0
    CHECK_FILES = auto()
    CHECK_MODULES = auto()
    LOAD_FILES = auto()
    LAUNCH = auto()
