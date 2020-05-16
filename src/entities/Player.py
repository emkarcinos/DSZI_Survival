import random

import pygame

from src.entities.Enums import Rotations, StatisticNames, Movement
from src.entities.Entity import Entity
from src.entities.Statistics import Statistics


class Player(Entity):
    def __init__(self, spawnpoint, size, affinities=None):
        """
        Create a player.

        :type affinities: Affinities
        :param spawnpoint: A tuple of coords (x,y)
        :param size: The size in px
        :param affinities: Affinities struct defining player's affinities
        """

        # Entity constructor
        super().__init__("player.png", size, spawnpoint, False)

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

        # Player can move only so fast
        self.moveTimeout = 100

        self.affinities = affinities

    def applyWalkingFatigue(self):
        """
        Lowers player's statistics. Applied every few steps.

        """
        # looses hunger every 10 steps taken
        if self.movePoints % 15 == 0:
            self.statistics.set_hunger(1)
        # gets more thirsty every 5 steps
        if self.movePoints % 10 == 0:
            self.statistics.set_thirst(2)
        # gets tired every step
        self.statistics.set_stamina(-1.5)

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

    def getStatistic(self, stat):
        """
        Get the specified statistic as an integer.

        :type stat: entities.Enums.StatisticNames
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
        elif self.statistics.stamina == 0:
            self.alive = False
            self.deathReason = StatisticNames.STAMINA

        # Change texture after dying
        if not self.alive:
            self.image, null = self.getTexture("gravestone.png", self.rect.h)

    def move(self, movement, interactableObject=None):
        """
        Overridden function. Adds fatigue to the movement.

        :param interactableObject: Object to interact with
        :type movement: entities.Enums.Movement
        :param movement: specify what movement should be done (See Movement enum)
        :return: Returns true, if the movement has succeeded
        """
        # Can move if timeout has elapsed
        if self.movementTimer > self.moveTimeout:
            self.movementTimer = 0
            # Movement
            if movement.value == Movement.FORWARD.value:
                self.moveForward()
                self.applyWalkingFatigue()
            # Interaction
            elif movement.value == Movement.PICKUP.value and interactableObject is not None:
                try:
                    interactableObject.on_interaction(self)
                except AttributeError:
                    pass
            # Rotation
            else:
                self.updateRotation(movement)
            return True
        else:
            return False

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
            self.updateEntityCoords()
            self.determineLife()
