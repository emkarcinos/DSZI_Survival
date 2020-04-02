import math
import pygame

# minimum UI width
MARGIN = 300


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
