from typing import Tuple

import pygame

from src.ui.UiElement import UiElement


class UiText(UiElement):
    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font = None,
                 textColor=(0, 0, 0), antialias: bool = False,
                 backgroundColor=None):
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

    def changeText(self, newText):
        self.text = newText

        if self.backgroundColor is not None:
            self.image.fill(self.backgroundColor)
        wordImage = self.font.render(self.text, self.antialias, self.textColor)
        self.image.blit(wordImage, (0, 0))
