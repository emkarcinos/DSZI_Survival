import math
from enum import Enum

import pygame

# minimum UI width
MARGIN = 300


# screen locations enum
class Locations(Enum):
    RIGHT_UI = 1
    LEFT_UI = 2
    MAP = 3


class Screen:
    def __init__(self, gameObject, windowConfig):
        self.gameObject = gameObject
        self.winX = windowConfig["width"]
        self.winY = windowConfig["height"]
        pygame.display.set_caption(windowConfig["name"])
        self.pygameScreen = pygame.display.set_mode((self.winX, self.winY))

        # map is a square inside the screen
        self.mapSize = self.calculateMapDimensions()

        # mapCoord is a top leftmost pixel
        self.mapCoord = math.floor((self.winX - self.mapSize) / 2)

        # draw a white rect to resemble map
        pygame.draw.rect(self.pygameScreen, (255, 255, 255), [self.mapCoord, 0, self.mapSize, self.mapSize])

    def calculateMapDimensions(self):
        result = 0
        expectedSize = self.winY

        # when there's not enough space for the UI on the sides
        if self.winX - expectedSize < MARGIN:
            result = expectedSize - (MARGIN - (self.winX - expectedSize))
        else:
            result = expectedSize

        return result

    # method to draw a sprite. Location param specifies where to draw the item (Locations enum)
    def draw(self, sprite, location, posX, posY):
        sprite.rect.x += posX
        sprite.rect.y += posY
        if location.value is Locations.RIGHT_UI.value:
            sprite.rect.x += self.mapCoord + self.mapSize
        elif location.value == Locations.MAP.value:
            sprite.rect.x += self.mapCoord
        self.gameObject.spritesList.add(sprite)

    def getUiWidth(self, location: Locations):
        if location is Locations.RIGHT_UI:
            return self.winX - (self.mapCoord + self.mapSize)
        elif location is Locations.LEFT_UI:
            return self.mapCoord
        elif location is Locations.MAP:
            return self.mapSize
