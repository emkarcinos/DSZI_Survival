from enum import Enum

from src.entities.Entity import Entity
from src.entities.Statistics import Statistics
import pygame


class Player(Entity):
    statistics: Statistics

    def __init__(self, spawnpoint, size):
        super().__init__("player.png", size, (spawnpoint[0] * size, spawnpoint[1] * size))
        # Where the player is facing, 0 - north, 1
        self.rotation = Rotations.NORTH
        self.statistics = Statistics(100, 0, 0, 100)

    # Move in a desired direction
    def move(self, rotation):
        self.statistics.set_stamina(-1)
        if rotation.value == Rotations.NORTH.value:
            self.rect.y -= self.rect.w
        elif rotation.value == Rotations.EAST.value:
            self.rect.x += self.rect.w
        elif rotation.value == Rotations.SOUTH.value:
            self.rect.y += self.rect.w
        elif rotation.value == Rotations.WEST.value:
            self.rect.x -= self.rect.w

    def getFacingCoord(self):
        if self.rotation == Rotations.NORTH:
            return (0, -1)
        elif self.rotation == Rotations.SOUTH:
            pass
    # Returns given statistic
    def getStatistic(self, stat):
        if stat.value == StatisticNames.HP:
            return self.statistics.hp
        elif stat.value == StatisticNames.HUNGER:
            return self.statistics.hunger
        elif stat.value == StatisticNames.THIRST:
            return self.statistics.thirst
        elif stat.value == StatisticNames.STAMINA:
            return self.statistics.stamina
        return None

    def getStatistics(self):
        return self.statistics

    def rotate(self, rotation):
        # If the player is not facing given direction, it will not move the first time, it will only get rotated
        if self.rotation.value != rotation.value:
            self.image = pygame.transform.rotate(self.image, ((self.rotation.value - rotation.value) * 90))
            self.rotation = rotation


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