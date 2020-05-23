from enum import Enum


class DistFromObject(Enum):
    """
    Distance in fields from object.

    """

    LT_3 = 0
    GE_3_LT_8 = 1
    GE_8 = 2
