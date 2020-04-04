import pygame

from src.ui.UiElement import UiElement


class UiConsole(UiElement):
    def __init__(self, rect: pygame.Rect, bgColor=(125, 125, 125)):
        super().__init__(rect)
        self.bgColor = bgColor

        self.image = pygame.Surface((rect.width, rect.height))
        self.image.fill(bgColor)
