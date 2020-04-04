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

        self.consoleLines = ["Hello from console!"]
        self.linesCount = 1
        self.linesImages = []
        self.linesImages.append(font.render(self.consoleLines[0], False, textColor))
        self.lineHeight = self.linesImages[0].get_height()

        self.maxLines = int(self.image.get_height() / self.lineHeight)


        self.__writeConsoleLines__()

    def __writeConsoleLines__(self, startingLineInd=0):
        self.image.fill(self.bgColor)
        writtenLines = 0
        for i in range(startingLineInd, min(self.maxLines + startingLineInd, self.linesCount)):
            self.image.blit(self.linesImages[i], (writtenLines*self.lineHeight, 0))
            writtenLines += 1
