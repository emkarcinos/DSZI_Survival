import random
from enum import Enum

import pygame

from src.entities.Entity import Entity
from src.entities.Statistics import Statistics


class Player(Entity):
    def __init__(self, spawnpoint, size):
        """
        :param spawnpoint: A tuple of coords relative to map
        :param size: The size in px
        """

        # Entity constructor
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

        self.alive = True
        # If a player dies, the death reason is stored here
        self.deathReason = None

        # Tracks time between every move
        self.movementTimer = 0

        # Player can move only so fast
        self.moveTimeout = 100

    def move(self, movement):
        """
        This function will attempt to move a player. It fails if the movement can not be done.
        :type movement: Movement
        :param movement: specify what movement should be done (See Movement enum)
        :return: Returns true, if the movement has succeeded
        """

        # Can move if timeout has elapsed
        if self.movementTimer > self.moveTimeout:
            self.movementTimer = 0
            # Rotation
            if movement.value != Movement.FORWARD.value:
                self.updateRotation(movement)
            # Else move
            else:
                self.moveForward()
            return True
        else:
            return False

    # Deprecated - use move() instead
    def moveForward(self):
        """
        Moves the player forward. NOTE: should not be used outside of the player class.
        """
        self.movePoints += 1
        # You can only move if you have enough stamina
        if self.statistics.stamina > 1:
            # self.applyWalkingFatigue()    # COMMENTED FOR A_START TEST
            if self.rotation.value == Rotations.NORTH.value:
                self.rect.y -= self.rect.w
            elif self.rotation.value == Rotations.EAST.value:
                self.rect.x += self.rect.w
            elif self.rotation.value == Rotations.SOUTH.value:
                self.rect.y += self.rect.w
            elif self.rotation.value == Rotations.WEST.value:
                self.rect.x -= self.rect.w

    def updateRotation(self, movement):
        """
        A method that rotates the player.
        :type movement: Movement
        :param movement: Rotation direction
        """
        if movement == Movement.ROTATE_L:
            self.rotate(Rotations((self.rotation.value - 1) % 4))
        elif movement == Movement.ROTATE_R:
            self.rotate(Rotations((self.rotation.value + 1) % 4))

    def rotate(self, rotation):
        """
        More low-level method than rotate - rotates the texture and updates the player
        rotation field.
        :type rotation: Movement
        :param rotation: 
        """
        # If the player is not facing given direction, it will not move the first time, it will only get rotated
        if self.rotation.value != rotation.value:
            self.image = pygame.transform.rotate(self.image, ((self.rotation.value - rotation.value) * 90))
            self.rotation = rotation

    def applyWalkingFatigue(self):
        """
        Lowers player's statistics.
        """
        # looses hunger every 10 steps taken
        if self.movePoints % 10 == 0:
            self.statistics.set_hunger(5)
        # gets more thirsty every 5 steps
        if self.movePoints % 5 == 0:
            self.statistics.set_thirst(6)
        # gets tired every step
        self.statistics.set_stamina(-2)

    def applyTimeFatigue(self, tickTime):
        """
        A separate method to lower the statistics. Invoked every frame.
        :param tickTime: Time passed between the previous frame (in milliseconds)
        """
        self.fatigueTimeout += tickTime
        if self.fatigueTimeout >= 700:
            self.statistics.set_thirst(5)
            self.statistics.set_hunger(3)
            # A player can randomly regenerate stamina
            if random.randrange(5) == 0:
                self.statistics.set_stamina(2)
            self.fatigueTimeout = 0

    # TODO: Remove
    def getFacingCoord(self):
        """
        Get coordinates forward to the player.
        :return: Position tuple
        """
        if self.rotation == Rotations.NORTH:
            return self.rect.x, self.rect.y - self.rect.h
        elif self.rotation == Rotations.SOUTH:
            return self.rect.x, self.rect.y + self.rect.h
        elif self.rotation == Rotations.EAST:
            return self.rect.x + self.rect.h, self.rect.y
        elif self.rotation == Rotations.WEST:
            return self.rect.x - self.rect.h, self.rect.y

    def getStatistic(self, stat):
        """
        Get the specified statistic as an integer.
        :type stat: StatisticNames
        :param stat: Which statistic to get
        :return: Int
        """
        if stat.value == StatisticNames.HP:
            return self.statistics.hp
        elif stat.value == StatisticNames.HUNGER:
            return self.statistics.hunger
        elif stat.value == StatisticNames.THIRST:
            return self.statistics.thirst
        elif stat.value == StatisticNames.STAMINA:
            return self.statistics.stamina
        return None

    # TODO: Useless?
    def getStatistics(self) -> Statistics:
        """
        Get the statistic object
        :return: Statistics
        """
        return self.statistics
        # Update player's rotation

    def determineLife(self):
        """
        Checks if the player is still alive, and sets the appropriate fields.
        Called every frame.
        """
        if self.statistics.hunger == 100:
            self.alive = False
            self.deathReason = StatisticNames.HUNGER
        elif self.statistics.thirst == 100:
            self.alive = False
            self.deathReason = StatisticNames.THIRST
        elif self.statistics.hp == 0:
            self.alive = False
            self.deathReason = StatisticNames.HP

        # Change texture after dying
        if not self.alive:
            self.image, null = self.getTexture("gravestone.png", self.rect.h)

    def update(self):
        """
        Called every frame
        """
        if self.alive:
            self.timeAlive += self.timer.get_time()
            # Player gets tired every once in a while
            # self.applyTimeFatigue(self.timer.get_time())   # COMMENTED FOR A_STAR_TEST
            # Adds frame time to movementTimer
            self.movementTimer += self.timer.tick()
            self.determineLife()


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
