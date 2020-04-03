import pygame

from src.ui.UiElement import UiElement


class UiBar(UiElement):
    def __init__(self, rect: pygame.Rect, initialFilledPercent=100, filledBarColor=(255, 0, 0), emptyBarColor=(0, 0, 0),
                 outlineColor=(75, 75, 75), outlineThickness=10):
        super().__init__(rect)
        self.filledPercent = initialFilledPercent / 100
        self.emptyBarColor = emptyBarColor
        self.barColor = filledBarColor

        self.image = pygame.Surface((rect.width, rect.height))

        filledPartRect = pygame.rect.Rect(outlineThickness / 2, outlineThickness / 2,
                                          (rect.width - outlineThickness) * self.filledPercent,
                                          rect.height - outlineThickness)
        self.image.fill(filledBarColor, filledPartRect)

        pygame.draw.rect(self.image, outlineColor, pygame.rect.Rect(0, 0, rect.width, rect.height),
                         outlineThickness)
