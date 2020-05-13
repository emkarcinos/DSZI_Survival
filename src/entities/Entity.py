from enum import Enum
from pathlib import Path

import pygame


# TODO: Add getters to retrieve relative coords
class Entity(pygame.sprite.Sprite):
    # Static ID counter - increments with each constructor call
    nextId = 1

    def __init__(self, texture, size, pos):
        """
        Create an entity.
        :param texture: Path to a file with texture
        :param size: Size in px
        :param pos: Position tuple
        """
        super().__init__()
        self.image, self.rect = self.getTexture(texture, size)
        self.image.set_colorkey((255, 255, 255))
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        # Unique ID
        self.id = self.setNewId()

        # Where the entity is facing
        self.rotation = Rotations.NORTH

    @staticmethod
    def setNewId():
        """
        Returns auto-incremented unique ID
        :return: ID Int
        """
        id = Entity.nextId
        Entity.nextId += 1
        return id

    @staticmethod
    def getTexture(textureName, tileSize):
        """
        Get the texture from a file. Texture path is pre-set to data/images/entities.
        :param textureName: Filename
        :param tileSize: Texture size (to scale to map size)
        :return: image, rect
        :rtype: pygame.image, pygame.rect
        """
        texturesFolder = ""
        textureFile = ""
        try:
            texturesFolder = Path("./data/images/entities")
            textureFile = texturesFolder / textureName
        except IOError:
            print("Cannot load texture from " + texturesFolder + ". Exiting...")
            exit(1)
        image = pygame.image.load(str(textureFile.resolve())).convert_alpha()
        image = pygame.transform.scale(image, (tileSize, tileSize))
        rect = image.get_rect()
        return image, rect

    def getFacingCoord(self):
        """
        Get coordinates forward to the player.
        :return: Position tuple
        """
        if self.rotation.value == Rotations.NORTH.value:
            return self.rect.x, self.rect.y - self.rect.h
        elif self.rotation.value == Rotations.SOUTH.value:
            return self.rect.x, self.rect.y + self.rect.h
        elif self.rotation.value == Rotations.EAST.value:
            return self.rect.x + self.rect.h, self.rect.y
        elif self.rotation.value == Rotations.WEST.value:
            return self.rect.x - self.rect.h, self.rect.y


class Rotations(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
