import pygame

from src.ui.UiElement import UiElement


class UiConsole(UiElement):
    def __init__(self, rect: pygame.Rect, bgColor=(125, 125, 125), textColor=(255, 255, 255), font=None):
        super().__init__(rect)
        self.textColor = textColor

        if font is None:
            font = pygame.font.Font(None, 25)
        self.font = font
        self.bgColor = bgColor

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

    def writeConsoleLines(self, startingLineInd=0):
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

    def addLinesToConsole(self, linesToAdd):
        for line in linesToAdd:
            self.consoleLines.append(line)
            self.linesCount += 1

            row = pygame.Surface((self.consoleWidth, self.lineHeight))
            row.fill(self.bgColor)

            howMuchRowIsFilled = 0
            words = line.split(' ')
            for word in words:
                wordImage = self.font.render(' ' + word, False, self.textColor)
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

    def addLinesToConsoleAndScrollToDisplayThem(self, linesToAdd):
        self.addLinesToConsole(linesToAdd)
        ind = 0
        if self.linesImagesCount > self.maxLines:
            ind = self.linesImagesCount - self.maxLines
        self.writeConsoleLines(ind)
