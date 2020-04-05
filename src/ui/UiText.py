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

        self.image = font.render(text, antialias, textColor, backgroundColor)
