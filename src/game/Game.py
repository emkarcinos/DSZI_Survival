import pygame
import json
from pathlib import Path


class Game:
    def __init__(self):
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


game = Game()
