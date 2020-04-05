from enum import Enum

import pygame

from src.entities.Statistics import Statistics
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
        self.timerTextView = UiText(pygame.Rect(0, 0, leftUiWidth, self.barHeight), font=self.font,
                                    text=timer.getPrettyTime(), textColor=Colors.WHITE.value,
                                    backgroundColor=Colors.GRAY.value)
        self.isDayTextView = UiText(
            pygame.Rect(0, self.timerTextView.rect.y + self.barHeight, leftUiWidth, self.barHeight), text="Day",
            font=self.font, backgroundColor=Colors.GRAY.value, textColor=Colors.WHITE.value)

        self.healthTextView = UiText(pygame.Rect(0, 0, rightUiWidth, self.barHeight), text="Health points",
                                     font=self.font, textColor=Colors.WHITE.value)
        self.healthBar = UiBar(
            pygame.Rect(0, self.healthTextView.rect.y + self.barHeight, rightUiWidth, self.barHeight))

        self.hungerTextView = UiText(
            pygame.Rect(0, self.healthBar.rect.y + self.barHeight, rightUiWidth, self.barHeight),
            text="Hunger", font=self.font, textColor=Colors.WHITE.value)
        self.hungerBar = UiBar(
            pygame.Rect(0, self.hungerTextView.rect.y + self.barHeight, rightUiWidth, self.barHeight),
            initialFilledPercent=0,
            filledBarColor=Colors.YELLOW.value)

        self.staminaTextView = UiText(
            pygame.Rect(0, self.hungerBar.rect.y + self.barHeight, rightUiWidth, self.barHeight), text="Stamina",
            font=self.font, textColor=Colors.WHITE.value)
        self.staminaBar = UiBar(
            pygame.Rect(0, self.staminaTextView.rect.y + self.barHeight, rightUiWidth, self.barHeight),
            filledBarColor=Colors.GREEN.value)

        self.thirstTextView = UiText(
            pygame.Rect(0, self.staminaBar.rect.y + self.barHeight, rightUiWidth, self.barHeight), text="Thirst",
            font=self.font, textColor=Colors.WHITE.value)
        self.thirstBar = UiBar(
            pygame.Rect(0, self.thirstTextView.rect.y + self.barHeight, rightUiWidth, self.barHeight),
            initialFilledPercent=0,
            filledBarColor=Colors.BLUE.value)

        self.console = UiConsole(pygame.Rect(0, self.timerTextView.rect.h + self.isDayTextView.rect.h, leftUiWidth,
                                             screenHeight - self.timerTextView.rect.h - self.isDayTextView.rect.h),
                                 font=self.font)

    def updateBasedOnPlayerStats(self, statistics: Statistics):
        consoleLines = []
        if self.healthBar.value != statistics.hp:
            self.healthBar.updateFill(statistics.hp)
            consoleLines.append("Health: " + str(statistics.hp))

        if self.hungerBar.value != statistics.hunger:
            self.hungerBar.updateFill(statistics.hunger)
            consoleLines.append("Hunger: " + str(statistics.hunger))

        if self.staminaBar.value != statistics.stamina:
            self.staminaBar.updateFill(statistics.stamina)
            consoleLines.append("Stamina: " + str(statistics.stamina))

        if self.thirstBar.value != statistics.thirst:
            self.thirstBar.updateFill(statistics.thirst)
            consoleLines.append("Stamina: " + str(statistics.thirst))

        self.console.addLinesToConsoleAndScrollToDisplayThem(consoleLines)

    def updateBasedOnPygameEvent(self, event: pygame.event):
        pass


class Colors(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    GRAY = (125, 125, 125)
