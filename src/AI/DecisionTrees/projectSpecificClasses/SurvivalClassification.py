from enum import Enum


class SurvivalClassification(Enum):
    """
    For example food classification means that player should go for food.
    """

    FOOD = 0
    WATER = 1
    REST = 2
