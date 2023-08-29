from enum import Enum

from PySide6.QtGui import QColorConstants

LOOP_INTERVAL_MSECS = 300
GUI_REFRESH_INTERVAL = 500


class outputTypesEnum(Enum):
    FEED = "Feed"
    GRAPH = "Graph"


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
    ADD_DATA_SOURCE = "Add Data Source"
    DATA_SOURCE_TYPE = "Data Source Type"
    DATA_SOURCE_SETTINGS = "Data Source Settings"
    DATA_SOURCE_PARAMETERS = "Data Source Parameters"
    CONFRIM_DATA_SOURCE = "Confirm Data Source"
    ADD_ACTION = "Add Action"
    ACTION_TYPE = "Action Type"
    ACTION_SETTINGS = "Action Settings"
    ACTION_PARAMETERS = "Action Parameters"
    CONFIRM_ACTION = "Confirm Action"
    FINAL_CONFIRM = "Final Confirm"
    SCRIPT_SETTINGS = "Script Settings"
    SCRIPT_PARAMETERS = "Script Parameters"


PROGRESS_BAR_HEIGHT = 10

PROGRESS_BAR_UNCOMPLETED_COLOR_STR = "#808080"
PROGRESS_BAR_UNCOMPLETED_COLOR = QColorConstants.DarkGray
PROGRESS_BAR_CURRENT_COLOR_STR = "#0000ff"
PROGRESS_BAR_CURRENT_COLOR = QColorConstants.Blue
PROGRESS_BAR_COMPLETED_COLOR_STR = "#00ff00"
PROGRESS_BAR_COMPLETED_COLOR = QColorConstants.Green
PROGRESS_BAR_FAILED_COLOR_STR = "#ff0000"
PROGRESS_BAR_FAILED_COLOR = QColorConstants.Red
