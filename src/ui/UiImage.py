from src.ui.UiElement import UiElement
import pygame


class UiImage(UiElement):
    def __init__(self, rect: pygame.Rect, image: pygame.Surface):
        super().__init__(rect)
        self.image = pygame.transform.scale(image, (rect.width, rect.height))
        

