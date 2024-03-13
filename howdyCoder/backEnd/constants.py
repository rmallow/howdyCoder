from enum import Enum, auto

"""
----------------------------
DATA SOURCE CONSTATNTS
----------------------------
"""


"""
----------------------------
FEED CONSTATNTS
----------------------------
"""


class FeedRetValues(Enum):
    VALID_VALUES = auto()
    NO_VALID_VALUES = auto()
    ALL_DS_FINISHED = auto()
    RESET_FEED = auto()
