import pygame
import json
from pathlib import Path

from game.Screen import Screen


class Game:
    def __init__(self):
        self.running = True
        print("Loading configuration...", end=" ")

        try:
            configFolder = Path("../../data/config/")
            configFile = configFolder / "mainConfig.json"

            self.config = json.loads(configFile.read_text())

            print("OK")
        except IOError:
            print("Error reading configuration file. Exiting...")
            exit(1)

        print("Initializing pygame...", end=" ")
        pygame.init()
        print("OK")

        print("Initializing screen, params: " + str(self.config["window"]) + "...", end=" ")

        # Vertical rotation is unsupported due to UI layout
        if self.config["window"]["height"] > self.config["window"]["width"]:
            print("The screen cannot be in a vertical orientation. Exiting...")
            exit(1)

        self.screen = Screen(self, self.config["window"])
        print("OK")

        self.spritesList = pygame.sprite.Group()

        self.mainLoop()

    def mainLoop(self):
        self.spritesList.draw(self.screen.pygameScreen)
        pygame.display.flip()


game = Game()
