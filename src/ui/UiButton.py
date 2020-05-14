from enum import Enum
from typing import Tuple, List, Any, Callable

import pygame
from pygame.font import FontType

from src.ui.UiElement import UiElement


class UiButton(UiElement):

    functionsToInvokeWhenClicked: List[Tuple[Callable, Any]]
    image: pygame.Surface
    beingClicked: bool
    text: str
    clickedBtnColor: Tuple[int, int, int]
    textColor: Tuple[int, int, int]
    font: pygame.font.Font

    def __init__(self, rect: pygame.Rect, notClickedBtnColor: Tuple[int, int, int] = (125, 125, 125),
                 clickedBtnColor: Tuple[int, int, int] = (255, 255, 255),
                 text: str = "Click", textColor: Tuple[int, int, int] = (0, 0, 0), font: pygame.font.Font = None,
                 functionsToInvokeWhenClicked: List[Tuple[Callable, Any]] = []):
        """
        Creates UiButton object.

        :param rect: Rectangle on which button will be displayed.
        :param notClickedBtnColor: Button color when it is not clicked.
        :param clickedBtnColor: Button color when it is clicked.
        :param text: Text to be displayed on button.
        :param textColor:
        :param font: Font for button text. If None is given then default font will be used.
        :type functionsToInvokeWhenClicked : list of tuple(function, args*), args are function arguments.
        """
        super().__init__(rect)
        if font is None:
            font = pygame.font.Font(None, 25)
        self.font = font
        self.textColor = textColor
        self.clickedBtnColor = clickedBtnColor
        self.notClickedBtnColor = notClickedBtnColor
        self.text = text
        self.__initBtnImages__()

        self.beingClicked = False
        self.image = self._images[0]

        self.functionsToInvokeWhenClicked = []

        self.functionsToInvokeWhenClicked.extend(functionsToInvokeWhenClicked)

    def eventHandler(self, event: pygame.event):
        """
        Checks if this button was clicked based on given pygame event.
        If yes, then it calls all functions that are on the list of functions to invoke.

        :param event: pygame event, which will be examined to check if this button was clicked.
        """
        # change selected color if this button's rectangle was clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):  # is mouse over button
                    self.image = self._images[ButtonImages.CLICKING_IMAGE.value]
                    self.beingClicked = True
                    for func, *args in self.functionsToInvokeWhenClicked:
                        func(*args)
        elif event.type == pygame.MOUSEBUTTONUP and self.beingClicked:
            if event.button == 1:
                self.beingClicked = False
                self.image = self._images[ButtonImages.DEFAULT_IMAGE.value]

    def __initBtnImages__(self) -> None:
        """
        Creates button images which will be drawn, so that button is displayed.

        """
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

    def addFuncToInvoke(self, tupleOfFuncAndArgs: Tuple[Callable, Any]) -> None:
        """
        Adds given function to list of functions, which will be invoked when this button is clicked.

        :type tupleOfFuncAndArgs: tuple(function, *args)
        """
        self.functionsToInvokeWhenClicked.append(tupleOfFuncAndArgs)


class ButtonImages(Enum):
    """
    This enum is used to display proper button images.
    When button is not clicked, then default image is being drawn.
    When button is clicked, clicking image is being drawn.
    """

    DEFAULT_IMAGE = 0
    CLICKING_IMAGE = 1
