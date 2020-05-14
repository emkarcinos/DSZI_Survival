import math
from enum import Enum

import pygame
from src.ui.Ui import Ui

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

        # TODO: Move to game / envents
        self.__initUi__()

    def calculateMapDimensions(self):
        result = 0
        expectedSize = self.winY

        # when there's not enough space for the UI on the sides
        if self.winX - expectedSize < MARGIN:
            result = expectedSize - (MARGIN - (self.winX - expectedSize))
        else:
            result = expectedSize

        return result

    def addSprite(self, sprite, location):
        """
        Adds a sprite to a screen at a given location
        :type location: Locations
        :param sprite: A sprite to add.
        :param location: Where should the sprite be displayed
        """
        if location.value is Locations.RIGHT_UI.value:
            sprite.rect.x += self.mapCoord + self.mapSize
        elif location.value == Locations.MAP.value:
            sprite.rect.x += self.mapCoord

        # Update Entities mapOffset field
        from src.entities.Entity import Entity
        if isinstance(sprite, Entity):
            sprite.mapOffset = self.mapCoord
        self.gameObject.spritesList.add(sprite)

    def getUiWidth(self, location: Locations):
        if location is Locations.RIGHT_UI:
            return self.winX - (self.mapCoord + self.mapSize)
        elif location is Locations.LEFT_UI:
            return self.mapCoord
        elif location is Locations.MAP:
            return self.mapSize

    # TODO: Move to game / events
    def __initUi__(self):
        self.ui = Ui(self.getUiWidth(Locations.RIGHT_UI), self.getUiWidth(Locations.LEFT_UI), self.winY,
                     self.gameObject.ingameTimer)
        self.addSprite(self.ui.timerTextView, Locations.LEFT_UI)
        self.addSprite(self.ui.isDayTextView, Locations.LEFT_UI)
        self.addSprite(self.ui.console, Locations.LEFT_UI)
        self.addSprite(self.ui.healthTextView, Locations.RIGHT_UI)
        self.addSprite(self.ui.healthBar, Locations.RIGHT_UI)
        self.addSprite(self.ui.hungerTextView, Locations.RIGHT_UI)
        self.addSprite(self.ui.hungerBar, Locations.RIGHT_UI)
        self.addSprite(self.ui.staminaTextView, Locations.RIGHT_UI)
        self.addSprite(self.ui.staminaBar, Locations.RIGHT_UI)
        self.addSprite(self.ui.thirstTextView, Locations.RIGHT_UI)
        self.addSprite(self.ui.thirstBar, Locations.RIGHT_UI)
