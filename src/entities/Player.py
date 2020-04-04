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


class Rotations(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3