from enum import Enum

from src.entities.Entity import Entity
from src.entities.Statistics import Statistics
import pygame


class Player(Entity, pygame.sprite.Sprite):
    def __init__(self, spawnpoint, size):
        pygame.sprite.Sprite.__init__(self)

        self.statistics = Statistics(100, 0, 0, 100)

        self.image, self.rect = Entity.getTexture("player.jpg", size)
        super(Player, self).__init__(self.image, spawnpoint)
        # Where the player is facing, 0 - north, 1
        self.rotation = Rotations.NORTH

    # Move in a desired direction
    def move(self, rotation):
        # If the player is not facing given direction, it will not move the first time, it will only get rotated
        if self.rotation.value != rotation.value:
            self.rotate(rotation)
        # Otherwise, move one tile to a given direction
        else:
            return 1

    def rotate(self, rotation):
        self.image = pygame.transform.rotate(self.image, (abs(self.rotation.value - rotation.value) * 90))
        self.rotation = rotation


class Rotations(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3