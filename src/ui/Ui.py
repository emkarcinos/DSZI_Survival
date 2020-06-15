from enum import Enum
from pathlib import Path
from typing import Union

import pygame

from src.entities.Enums import StatisticNames
from src.entities.Interactable import Interactable
from src.entities.Pickupable import Pickupable
from src.entities.Player import Player
from src.entities.Statistics import Statistics
from src.game.Timer import Timer
from src.ui.UiBar import UiBar
from src.ui.UiConsole import UiConsole
from src.ui.UiText import UiText


class Ui:
    elements: pygame.sprite.Group
    timer: Timer
    antialias: bool
    barHeight: float

    def __init__(self, rightUiWidth: int, leftUiWidth: int, screenHeight: int, timer: Timer,
                 font: Union[pygame.font.Font, None] = None, antialias: bool = True):
        """
        Creates Ui object. Instantiates all UI elements.

        :param rightUiWidth:
        :param leftUiWidth:
        :param screenHeight:
        :param timer:
        :param font:
        :param antialias:
        """
        self.elements = pygame.sprite.Group()

        self.leftUiWidth = leftUiWidth
        self.rightUiWidth = rightUiWidth
        self.screenHeight = screenHeight

        # Default bar's height, like hp bar.
        self.barHeight = 25

        self.antialias = antialias

        # If no font was given then load it from predefined file.
        if font is None:
            font = self.__loadFont__()
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

    def __loadFont__(self) -> pygame.font.Font:
        """
        Loads project's default font.

        :return: Font loaded from file.
        """
        fontName = "FiraCode-Light.ttf"
        fontFolder = ""
        fontFile = ""
        try:
            fontFolder = Path("./data/fonts")
            fontFile = fontFolder / fontName
        except IOError:
            print("Cannot load font from " + fontFolder + ". Exiting...")
            exit(1)
        fontPath = str(fontFile.resolve())
        font = pygame.font.Font(fontPath, int(self.barHeight / 1.5))
        return font

    def updateConsoleBasedOnPlayerStats(self, statistics: Statistics):
        """
        Prints statistics on console.

        :param statistics: Statistics to print
        """
        consoleLines = ["Health: " + str(statistics.hp), "Hunger: " + str(statistics.hunger),
                        "Stamina: " + str(statistics.stamina), "Thirst: " + str(statistics.thirst)]

        for line in consoleLines:
            self.console.printToConsole(line)

    def updateBarsBasedOnPlayerStats(self, statistics: Statistics):
        """
        Updates bars like hp bar to match player's statistics.

        :param statistics:
        """
        self.healthBar.updateFill(statistics.hp)
        self.hungerBar.updateFill(statistics.hunger)
        self.staminaBar.updateFill(statistics.stamina)
        self.thirstBar.updateFill(statistics.thirst)

    def updateBasedOnPygameEvent(self, event: pygame.event):
        """
        Examines event and does actions:
            - console scrolling

        :param event: pygame event to examine.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            console = self.console
            if event.button == 4:
                console.scrollDown()
            elif event.button == 5:
                console.scrollUp()

    def updateOnPlayerPickup(self, playerStats, pickedObject: Pickupable):
        """
        This method should be called to update UI state after player pickup.
        Given player statistics and picked object updates bars and prints message to console.

        :param playerStats:
        :param pickedObject:
        """
        self.console.printToConsole(self.timer.getPrettyTime() + " - Picked object " + str(pickedObject.id) + ":")
        self.updateConsoleBasedOnPlayerStats(playerStats)

    def updateOnPlayerInteraction(self, playerStats, interactedObject: Interactable):
        """
        This method should be called to update UI state after player interaction.
        Updates bars and prints message to console.

        :param playerStats:
        :param interactedObject:
        """
        self.console.printToConsole(self.timer.getPrettyTime() + " - Player interacted with " + str(interactedObject.id) + ":")
        self.updateConsoleBasedOnPlayerStats(playerStats)

    def updateOnDeath(self, player: Player):
        """
        Updates UI after player death. Prints death reason to console.

        :param player: Dead player.
        """
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
        else:
            deathReasonString = "Wrong food recognition"

        consoleLines.append("Death reason: " + deathReasonString)

        consoleLines.append("Time alive: " + str(player.timeAlive / 1000) + "s")

        for line in consoleLines:
            self.console.printToConsole(line)

    def updateTime(self):
        """
        Updates timer and changes text eventually changes day or night text.

        """
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
