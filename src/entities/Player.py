from enum import Enum
import random

from src.entities.Entity import Entity
from src.entities.Statistics import Statistics
import pygame


class Player(Entity):
    def __init__(self, spawnpoint, size):
        super().__init__("player.png", size, (spawnpoint[0] * size, spawnpoint[1] * size))
        # Where the player is facing, 0 - north, 1
        self.rotation = Rotations.NORTH
        self.statistics = Statistics(100, 0, 0, 100)
        # How many steps has the player taken through its lifetime
        self.movePoints = 0
        # Tracks how much time has passed since the player is alive
        self.timer = pygame.time.Clock()
        self.timeAlive = 1
        # Used to determine fatigue
        self.fatigueTimeout = 0

    # Move in a desired direction
    def move(self, rotation):
        self.movePoints += 1
        # You can only move if you have enough stamina
        if self.statistics.stamina > 1:
            self.applyWalkingFatigue()
            if rotation.value == Rotations.NORTH.value:
                self.rect.y -= self.rect.w
            elif rotation.value == Rotations.EAST.value:
                self.rect.x += self.rect.w
            elif rotation.value == Rotations.SOUTH.value:
                self.rect.y += self.rect.w
            elif rotation.value == Rotations.WEST.value:
                self.rect.x -= self.rect.w

    def applyWalkingFatigue(self):
        # looses hunger every 10 steps taken
        if self.movePoints % 10 == 0:
            self.statistics.set_hunger(5)
        # gets more thirsty every 5 steps
        if self.movePoints % 5 == 0:
            self.statistics.set_thirst(6)
        # gets tired every step
        self.statistics.set_stamina(-2)

    def applyTimeFatigue(self, tickTime):
        self.fatigueTimeout += tickTime
        if self.fatigueTimeout >= 700:
            self.statistics.set_thirst(5)
            self.statistics.set_hunger(3)
            # A player can randomly regenerate stamina
            if random.randrange(5) == 0:
                self.statistics.set_stamina(2)
            self.fatigueTimeout = 0


    def getFacingCoord(self):
        if self.rotation == Rotations.NORTH:
            return self.rect.x, self.rect.y - (self.rect.h)
        elif self.rotation == Rotations.SOUTH:
            return self.rect.x, self.rect.y + (self.rect.h)
        elif self.rotation == Rotations.EAST:
            return self.rect.x + (self.rect.h), self.rect.y
        elif self.rotation == Rotations.WEST:
            return self.rect.x - (self.rect.h), self.rect.y

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

    # Called every frame
    def update(self):
        self.timeAlive += self.timer.get_time()
        # Player gets tired every once in a while
        self.applyTimeFatigue(self.timer.get_time())
        self.timer.tick()


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