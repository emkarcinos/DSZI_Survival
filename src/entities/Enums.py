from enum import Enum


class Rotations(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class StatisticNames(Enum):
    HP = 0
    STAMINA = 1
    HUNGER = 2
    THIRST = 3


class Movement(Enum):
    ROTATE_R = 0
    ROTATE_L = 1
    FORWARD = 2
    PICKUP = 3

class Classifiers(Enum):
    FOOD = 0
    WATER = 1
    REST = 2
    HERB = 3
