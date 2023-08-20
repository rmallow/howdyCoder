from .util.nameMatchEnum import nameMatchEnum
from enum import Enum

"""
----------------------------
DATA SOURCE CLASS CONSTATNTS
----------------------------
"""


class DataSourceTypeEnum(nameMatchEnum):
    HISTORICAL_REQUEST = 1
    REAL_TIME_REQUEST = 2
    CSV = 3
    DIR = 4
    URL = 5


class DataSourceReturnEnum(nameMatchEnum):
    NO_DATA = 0
    END_DATA = 1
    OUTSIDE_CONSTRAINT = 2


class FeedRetValues(Enum):
    VALID_VALUES = 0
    NO_VALID_VALUES = 1


"""
----------------------------
FEED CONSTANTS
----------------------------
"""

INSUF_DATA = "insufData"

COL_NF = "colNF"
