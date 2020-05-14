import pygame


class UiElement(pygame.sprite.Sprite):
    rect: pygame.Rect

    def __init__(self, rect: pygame.Rect):
        """
        Creates UiElement object.
        :param rect: UiElement will be drawn on this rectangle.
        """
        super().__init__()
        self.rect = rect
