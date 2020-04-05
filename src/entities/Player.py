from enum import Enum

from src.entities.Entity import Entity
from src.entities.Statistics import Statistics
import pygame


class Player(Entity):
    def __init__(self, spawnpoint, size):
        super().__init__("player.jpg", size, spawnpoint)
        # Where the player is facing, 0 - north, 1
        self.rotation = Rotations.NORTH

    # Move in a desired direction
    def move(self, rotation):
        # If the player is not facing given direction, it will not move the first time, it will only get rotated
        if self.rotation.value != rotation.value:
            self.rotate(rotation)
        # Otherwise, move one tile to a given direction
        else:
            # TODO: Collision checks "and not to events"
            if rotation.value == Rotations.NORTH.value:
                self.rect.y -= self.rect.w
            elif rotation.value == Rotations.EAST.value:
                self.rect.x += self.rect.w
            elif rotation.value == Rotations.SOUTH.value:
                self.rect.y += self.rect.w
            elif rotation.value == Rotations.WEST.value:
                self.rect.x -= self.rect.w

    def rotate(self, rotation):
        self.image = pygame.transform.rotate(self.image, ((self.rotation.value - rotation.value) * 90))
        self.rotation = rotation

class Rotations(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3