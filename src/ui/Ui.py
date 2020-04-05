from enum import Enum

import pygame

from src.ui.UiBar import UiBar
from src.ui.UiConsole import UiConsole
from src.ui.UiText import UiText


class Ui():
    def __init__(self, rightUiWidth, leftUiWidth, screenHeight, timer, font=None):
        self.elements = pygame.sprite.Group()

        self.leftUiWidth = leftUiWidth
        self.rightUiWidth = rightUiWidth
        self.screenHeight = screenHeight

        self.barHeight = 25

        if font is None:
            font = pygame.font.Font(None, self.barHeight)
        self.font = font

        self.timer = timer
        self.timerTextView = UiText(pygame.Rect(0, 0, leftUiWidth, self.barHeight), textColor=Colors.WHITE,
                                    backgroundColor=Colors.GRAY)

        self.isDayTextView = UiText(pygame.Rect(0, 0, leftUiWidth, self.barHeight), font=self.font)

        self.healthBar = UiBar(pygame.Rect(0, 0, rightUiWidth, self.barHeight))
        self.hungerBar = UiBar(pygame.Rect(0, 0, rightUiWidth, self.barHeight), initialFilledPercent=0,
                               filledBarColor=Colors.YELLOW)
        self.staminaBar = UiBar(pygame.Rect(0, 0, rightUiWidth, self.barHeight), filledBarColor=Colors.GREEN)
        self.thirstBar = UiBar(pygame.Rect(0, 0, rightUiWidth, self.barHeight), initialFilledPercent=0,
                               filledBarColor=Colors.BLUE)

        self.healthTextView = UiText(pygame.Rect(0, 0, rightUiWidth, self.barHeight), text="Health points",
                                     font=self.font, textColor=Colors.WHITE)

        self.hungerTextView = UiText(pygame.Rect(0, 0, rightUiWidth, self.barHeight), text="Hunger",
                                     font=self.font, textColor=Colors.WHITE)

        self.staminaTextView = UiText(pygame.Rect(0, 0, rightUiWidth, self.barHeight), text="Stamina",
                                      font=self.font, textColor=Colors.WHITE)

        self.thirstTextView = UiText(pygame.Rect(0, 0, rightUiWidth, self.barHeight), text="Thirst",
                                     font=self.font, textColor=Colors.WHITE)

        self.console = UiConsole(pygame.Rect(0, 0, leftUiWidth,
                                             screenHeight - self.timerTextView.rect.h - self.isDayTextView.rect.h))


class Colors(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    GRAY = (125, 125, 125)
