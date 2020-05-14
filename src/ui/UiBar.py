from typing import Tuple

import pygame

from src.ui.UiElement import UiElement


class UiBar(UiElement):
    filledBarColor: Tuple[int, int, int]
    outlineThickness: int
    outlineColor: Tuple[int, int, int]
    emptyBarColor: Tuple[int, int, int]
    filledPercent: int

    def __init__(self, rect: pygame.Rect, initialFilledPercent: int = 100,
                 filledBarColor: Tuple[int, int, int] = (255, 0, 0), emptyBarColor: Tuple[int, int, int] = (0, 0, 0),
                 outlineColor: Tuple[int, int, int] = (75, 75, 75), outlineThickness: int = 10):
        """
        Creates UiBar object
        :param rect:
        :param initialFilledPercent: How much bar is filled at the beginning. Number between 0 and 100
        :param filledBarColor: Color of the filled part of the bar.
        :param emptyBarColor: Color of the empty part of the bar.
        :param outlineColor: Color of the bar outline.
        :param outlineThickness:
        """
        super().__init__(rect)

        # Make sure that filled percent is between 0 and 100
        if initialFilledPercent < 0:
            initialFilledPercent = 0
        elif initialFilledPercent > 100:
            initialFilledPercent = 100
        self.filledPercent = initialFilledPercent

        self.emptyBarColor = emptyBarColor
        self.barColor = filledBarColor
        self.outlineColor = outlineColor
        self.outlineThickness = outlineThickness
        self.filledBarColor = filledBarColor

        self.__genBar__()

    def __genBar__(self):
        """
        Generates bar image based on filled percent field.
        """
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        filledPartRect = pygame.rect.Rect(self.outlineThickness / 2, self.outlineThickness / 2,
                                          (self.rect.width - self.outlineThickness) * (self.filledPercent / 100),
                                          self.rect.height - self.outlineThickness)
        self.image.fill(self.filledBarColor, filledPartRect)
        pygame.draw.rect(self.image, self.outlineColor, pygame.rect.Rect(0, 0, self.rect.width, self.rect.height),
                         self.outlineThickness)

    def updateFill(self, filledPercent: int):
        """
        Updates how much bar is filled
        :param filledPercent: Value between 0 and 100
        """
        self.filledPercent = filledPercent
        self.__genBar__()
