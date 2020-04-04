import pygame

from src.ui.UiElement import UiElement


class UiButton(UiElement):

    def __init__(self, rect: pygame.Rect, text="Click", color=(125, 125, 125)):
        super().__init__(rect)
        self.text = text
        self.color = color

        self.DEFAULTIMAGE = 0
        self.CLICKINGIMAGE = 1

        self._images = [
            pygame.Surface((rect.width, rect.height)),
            pygame.Surface((rect.width, rect.height)),
        ]

        # fill images with color - red, gree, blue
        self._images[0].fill((255, 0, 0))
        self._images[1].fill((0, 255, 0))

        self.beingClicked = False

        self.image = self._images[0]

    def eventHandler(self, event):

        # change selected color if rectange clicked
        if event.type == pygame.MOUSEBUTTONDOWN:  # is some button clicked
            if event.button == 1:  # is left button clicked
                if self.rect.collidepoint(event.pos):  # is mouse over button

                    self.image = self._images[self.CLICKINGIMAGE]
                    self.beingClicked = True
        elif event.type == pygame.MOUSEBUTTONUP and self.beingClicked:
            if event.button == 1:
                self.beingClicked = False
                self.image = self._images[self.DEFAULTIMAGE]
