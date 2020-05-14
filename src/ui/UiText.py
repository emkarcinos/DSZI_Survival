from typing import Tuple, Union

import pygame
from pygame.font import FontType

from src.ui.UiElement import UiElement


class UiText(UiElement):
    image: pygame.Surface
    font: pygame.font.Font
    text: str
    antialias: bool
    textColor: Tuple[int, int, int]
    backgroundColor: Tuple[int, int, int]

    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font = None,
                 textColor: Tuple[int, int, int] = (0, 0, 0), antialias: bool = False,
                 backgroundColor: Union[Tuple[int, int, int], None] = None):
        """
        Creates UiText object.

        :param rect: Rectangle on which text view will be drawn.
        :param text:
        :param font: If no font is given then default pygame font will be used.
        :param textColor:
        :param antialias:
        :param backgroundColor: Can be None.
        """
        super().__init__(rect)

        self.backgroundColor = backgroundColor
        self.antialias = antialias
        self.textColor = textColor
        self.text = text
        if font is None:
            font = pygame.font.Font(None, 12)
        self.font = font

        self.image = pygame.Surface((rect.w, rect.h))
        if backgroundColor is not None:
            self.image.fill(backgroundColor)
        wordImage = self.font.render(text, antialias, textColor)
        self.image.blit(wordImage, (0, 0))

    def changeText(self, newText: str):
        """
        Changes text view's text.

        :param newText:
        """
        self.text = newText

        if self.backgroundColor is not None:
            self.image.fill(self.backgroundColor)
        wordImage = self.font.render(self.text, self.antialias, self.textColor)
        self.image.blit(wordImage, (0, 0))
