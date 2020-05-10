import pygame
from typing import Tuple, List
from pygame.font import FontType

from src.ui.UiElement import UiElement


class UiConsole(UiElement):
    linesCount: int
    antialias: bool
    bgColor: Tuple[int, int, int]
    font: pygame.font.Font
    maxLines: int
    lineHeight: int
    linesImages: List[pygame.Surface]
    topWrittenLineInd: int
    consoleLines: List[str]
    linesImagesCount: int
    consoleWidth: float
    image: pygame.Surface

    def __init__(self, rect: pygame.Rect, bgColor: Tuple[int, int, int] = (125, 125, 125),
                 textColor: Tuple[int, int, int] = (255, 255, 255), font: pygame.font.Font = None, antialias: bool = True):
        super().__init__(rect)
        self.textColor = textColor

        if font is None:
            font = pygame.font.Font(None, 25)
        self.font = font
        self.bgColor = bgColor
        self.antialias = antialias

        self.image = pygame.Surface((rect.width, rect.height))
        self.image.fill(bgColor)

        self.consoleWidth = self.image.get_width()
        self.linesImagesCount = 0

        self.consoleLines = []
        self.linesCount = 0
        self.topWrittenLineInd = 0

        self.linesImages = []
        self.lineHeight = font.render("sampleText", False, textColor).get_height()

        self.maxLines = int(self.image.get_height() / self.lineHeight)

        self.addLinesToConsole(["Hello from console!"])
        self.writeConsoleLines()

    # TODO: Should this method be static? We need to instantiate some console before we can write anything to it.
    def writeToConsole(self, inp: str):
        """
        Writes given string to console and scrolls (console) down to display it.
        :param inp: String to be written to console.
        """
        self.addLinesToConsoleAndScrollToDisplayThem([inp])

    def writeConsoleLines(self, startingLineInd: int = 0):
        """
        Displays lines stored in console's list of lines, starting from line with given index.
        :param startingLineInd: Line index, which will be written on top of the console.
        """
        self.image.fill(self.bgColor)
        if startingLineInd < 0:
            startingLineInd = 0
        elif startingLineInd >= self.linesImagesCount:
            startingLineInd = self.linesImagesCount - 1
        self.topWrittenLineInd = startingLineInd
        writtenLines = 0
        for i in range(startingLineInd, min(self.maxLines + startingLineInd, self.linesImagesCount)):
            self.image.blit(self.linesImages[i], (0, writtenLines * self.lineHeight))
            writtenLines += 1

    def addLinesToConsole(self, linesToAdd: List[str]):
        """
        Adds lines to console's list of lines. If one line is too long to display, then it is being cut to pieces,
        so that it is appropriate size.

        Warning: this method doesn't display given lines, just adds to list of lines.
        :param linesToAdd:
        """
        for line in linesToAdd:
            self.consoleLines.append(line)
            self.linesCount += 1

            row = pygame.Surface((self.consoleWidth, self.lineHeight))
            row.fill(self.bgColor)

            howMuchRowIsFilled = 0
            words = line.split(' ')
            for word in words:
                wordImage = self.font.render(' ' + word, self.antialias, self.textColor)
                if howMuchRowIsFilled + wordImage.get_width() <= self.consoleWidth:
                    row.blit(wordImage, (howMuchRowIsFilled, 0))
                    howMuchRowIsFilled += wordImage.get_width()
                else:
                    self.linesImages.append(row)
                    self.linesImagesCount += 1
                    row = pygame.Surface((self.consoleWidth, self.lineHeight))
                    row.fill(self.bgColor)
                    howMuchRowIsFilled = 0

                    row.blit(wordImage, (howMuchRowIsFilled, 0))
                    howMuchRowIsFilled += wordImage.get_width()

            self.linesImages.append(row)
            self.linesImagesCount += 1

    def addLinesToConsoleAndScrollToDisplayThem(self, linesToAdd: List[str]):
        """
        Adds given lines to console's list of lines, writes them and scrolls console down to display them.
        :param linesToAdd: Lines to add to console's list of lines and to display.
        """
        self.addLinesToConsole(linesToAdd)
        ind = 0
        if self.linesImagesCount > self.maxLines:
            ind = self.linesImagesCount - self.maxLines
        self.writeConsoleLines(ind)
