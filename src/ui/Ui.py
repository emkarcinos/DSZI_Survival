from enum import Enum
from pathlib import Path

import pygame

from src.entities.Enums import StatisticNames
from src.entities.Statistics import Statistics
from src.ui.UiBar import UiBar
from src.ui.UiConsole import UiConsole
from src.ui.UiText import UiText


class Ui():
    def __init__(self, rightUiWidth, leftUiWidth, screenHeight, timer, font=None, antialias=True):
        self.elements = pygame.sprite.Group()

        self.leftUiWidth = leftUiWidth
        self.rightUiWidth = rightUiWidth
        self.screenHeight = screenHeight

        self.barHeight = 25

        self.antialias = antialias

        fontName = "FiraCode-Light.ttf"
        fontFolder = ""
        fontFile = ""
        try:
            fontFolder = Path("./data/fonts")
            fontFile = fontFolder / fontName
        except IOError:
            print("Cannot load texture from " + fontFolder + ". Exiting...")
            exit(1)
        fontPath = str(fontFile.resolve())
        if font is None:
            font = pygame.font.Font(fontPath, int(self.barHeight / 1.5))
        self.font = font

        self.timer = timer
        self.timerTextView = UiText(pygame.Rect(0, 0, leftUiWidth, self.barHeight), font=self.font,
                                    text=timer.getPrettyTime(), textColor=Colors.WHITE.value,
                                    backgroundColor=Colors.GRAY.value, antialias=self.antialias)
        self.isDayTextView = UiText(
            pygame.Rect(0, self.timerTextView.rect.y + self.barHeight, leftUiWidth, self.barHeight), text="Day",
            font=self.font, backgroundColor=Colors.GRAY.value, textColor=Colors.WHITE.value, antialias=self.antialias)

        self.healthTextView = UiText(pygame.Rect(0, 0, rightUiWidth, self.barHeight), text="Health points",
                                     font=self.font, textColor=Colors.WHITE.value, antialias=self.antialias)
        self.healthBar = UiBar(
            pygame.Rect(0, self.healthTextView.rect.y + self.barHeight, rightUiWidth, self.barHeight))

        self.hungerTextView = UiText(
            pygame.Rect(0, self.healthBar.rect.y + self.barHeight, rightUiWidth, self.barHeight),
            text="Hunger", font=self.font, textColor=Colors.WHITE.value, antialias=self.antialias)
        self.hungerBar = UiBar(
            pygame.Rect(0, self.hungerTextView.rect.y + self.barHeight, rightUiWidth, self.barHeight),
            initialFilledPercent=0,
            filledBarColor=Colors.YELLOW.value)

        self.staminaTextView = UiText(
            pygame.Rect(0, self.hungerBar.rect.y + self.barHeight, rightUiWidth, self.barHeight), text="Stamina",
            font=self.font, textColor=Colors.WHITE.value, antialias=self.antialias)
        self.staminaBar = UiBar(
            pygame.Rect(0, self.staminaTextView.rect.y + self.barHeight, rightUiWidth, self.barHeight),
            filledBarColor=Colors.GREEN.value)

        self.thirstTextView = UiText(
            pygame.Rect(0, self.staminaBar.rect.y + self.barHeight, rightUiWidth, self.barHeight), text="Thirst",
            font=self.font, textColor=Colors.WHITE.value, antialias=self.antialias)
        self.thirstBar = UiBar(
            pygame.Rect(0, self.thirstTextView.rect.y + self.barHeight, rightUiWidth, self.barHeight),
            initialFilledPercent=0,
            filledBarColor=Colors.BLUE.value)

        self.console = UiConsole(pygame.Rect(0, self.timerTextView.rect.h + self.isDayTextView.rect.h, leftUiWidth,
                                             screenHeight - self.timerTextView.rect.h - self.isDayTextView.rect.h),
                                 font=self.font, antialias=self.antialias)

    def updateConsoleBasedOnPlayerStats(self, statistics: Statistics):
        consoleLines = ["Health: " + str(statistics.hp), "Hunger: " + str(statistics.hunger),
                        "Stamina: " + str(statistics.stamina), "Thirst: " + str(statistics.thirst)]
        self.console.addLinesToConsoleAndScrollToDisplayThem(consoleLines)

    def updateBarsBasedOnPlayerStats(self, statistics: Statistics):
        self.healthBar.updateFill(statistics.hp)
        self.hungerBar.updateFill(statistics.hunger)
        self.staminaBar.updateFill(statistics.stamina)
        self.thirstBar.updateFill(statistics.thirst)

    def updateBasedOnPygameEvent(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            console = self.console
            if event.button == 4:
                console.scrollDown()
            elif event.button == 5:
                console.scrollUp()

    def updateOnPlayerPickup(self, playerStats, pickedObject):
        self.console.addLinesToConsoleAndScrollToDisplayThem([self.timer.getPrettyTime() + " - Picked object " + str(pickedObject.id) + ":"])
        self.updateConsoleBasedOnPlayerStats(playerStats)

    def updateOnPlayerInteraction(self, playerStats, interactedObject):
        self.console.addLinesToConsoleAndScrollToDisplayThem([self.timer.getPrettyTime() + " - Player interacted with " + str(interactedObject.id) + ":"])
        self.updateConsoleBasedOnPlayerStats(playerStats)

    def updateOnDeath(self, player):
        consoleLines = []

        deathReason: StatisticNames = player.deathReason

        consoleLines.append(self.timer.getPrettyTime() + " - Game Over")
        deathReasonString = ""
        if deathReason is StatisticNames.HP:
            deathReasonString = "Health issues"
        elif deathReason is StatisticNames.HUNGER:
            deathReasonString = "Hunger"
        elif deathReason is StatisticNames.STAMINA:
            deathReasonString = "Exhaustion"
        elif deathReason is StatisticNames.THIRST:
            deathReasonString = "Dehydration"

        consoleLines.append("Death reason: " + deathReasonString)

        consoleLines.append("Time alive: " + str(player.timeAlive / 1000) + "s")

        self.console.addLinesToConsoleAndScrollToDisplayThem(consoleLines)

    def updateTime(self):
        self.timerTextView.changeText(self.timer.getPrettyTime())
        if self.timer.isItDay():
            self.isDayTextView.changeText("Day")
        else:
            self.isDayTextView.changeText("Night")


class Colors(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    GRAY = (125, 125, 125)
