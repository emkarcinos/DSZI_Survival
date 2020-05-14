from src.ui.UiElement import UiElement
import pygame


class UiImage(UiElement):
    image: pygame.Surface

    def __init__(self, rect: pygame.Rect, image: pygame.Surface):
        """
        Creates UiImage object.
        :param rect: Rectangle on which image will be displayed
        :param image: Image to display
        """
        super().__init__(rect)
        self.image = pygame.transform.scale(image, (rect.width, rect.height))
        

