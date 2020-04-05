import pygame

from src.ui.UiElement import UiElement


class UiBar(UiElement):
    def __init__(self, rect: pygame.Rect, initialFilledPercent=100, filledBarColor=(255, 0, 0), emptyBarColor=(0, 0, 0),
                 outlineColor=(75, 75, 75), outlineThickness=10):
        super().__init__(rect)
        self.filledPercent = initialFilledPercent / 100
        self.emptyBarColor = emptyBarColor
        self.barColor = filledBarColor
        self.outlineColor = outlineColor
        self.outlineThickness = outlineThickness
        self.filledBarColor = filledBarColor

        self.__genBar__()

    def __genBar__(self):
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        filledPartRect = pygame.rect.Rect(self.outlineThickness / 2, self.outlineThickness / 2,
                                          (self.rect.width - self.outlineThickness) * self.filledPercent,
                                          self.rect.height - self.outlineThickness)
        self.image.fill(self.filledBarColor, filledPartRect)
        pygame.draw.rect(self.image, self.outlineColor, pygame.rect.Rect(0, 0, self.rect.width, self.rect.height),
                         self.outlineThickness)

    def updateFill(self, filledPercent):
        self.filledPercent = filledPercent / 100
        self.__genBar__()
