from enum import IntFlag, auto

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


class FeedRetFlag(IntFlag):
    NO_VALID_VALUES = 0
    VALID_VALUES = auto()
    ALL_DS_FINISHED = auto()
    RESET_FEED = auto()
