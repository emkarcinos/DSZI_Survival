from enum import Enum

import pygame

from src.ui.UiElement import UiElement


class UiButton(UiElement):

    def __init__(self, rect: pygame.Rect, notClickedBtnColor=(125, 125, 125), clickedBtnColor=(255, 255, 255),
                 text="Click", textColor=(0, 0, 0), font=None):
        super().__init__(rect)
        if font is None:
            self.font = pygame.font.Font(None, 25)
        self.textColor = textColor
        self.clickedBtnColor = clickedBtnColor
        self.notClickedBtnColor = notClickedBtnColor
        self.text = text
        self.__initBtnImages__()

        self.beingClicked = False
        self.image = self._images[0]

    def eventHandler(self, event):
        # change selected color if rectangle clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):  # is mouse over button
                    self.image = self._images[ButtonImages.CLICKING_IMAGE.value]
                    self.beingClicked = True
        elif event.type == pygame.MOUSEBUTTONUP and self.beingClicked:
            if event.button == 1:
                self.beingClicked = False
                self.image = self._images[ButtonImages.DEFAULT_IMAGE.value]

    def __initBtnImages__(self):
        self._images = [
            pygame.Surface((self.rect.width, self.rect.height)),
            pygame.Surface((self.rect.width, self.rect.height)),
        ]
        self._images[ButtonImages.DEFAULT_IMAGE.value].fill(self.notClickedBtnColor)
        self._images[ButtonImages.CLICKING_IMAGE.value].fill(self.clickedBtnColor)
        self.textSurface = self.font.render(self.text, False, (0, 0, 0))
        self.textSurfaceDest = (self.rect.centerx - (self.textSurface.get_width() / 2),
                                self.rect.centery - (self.textSurface.get_height() / 2))
        self._images[0].blit(self.textSurface, self.textSurfaceDest)
        self._images[1].blit(self.textSurface, self.textSurfaceDest)


class ButtonImages(Enum):
    DEFAULT_IMAGE = 0
    CLICKING_IMAGE = 1
