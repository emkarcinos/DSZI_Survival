import pygame
import json
from pathlib import Path
from os import path

from game.EventManager import EventManager
from game.Screen import Screen
from game.Map import Map

from src.entities.Pickupable import Pickupable
from src.entities.Player import Player
from src.entities.Statistics import Statistics


class Game:
    def __init__(self):
        self.running = True
        print("Loading configuration...", end=" ")

        try:
            configFolder = Path("../data/config/")
            configFile = configFolder / "mainConfig.json"

            self.config = json.loads(configFile.read_text())

            print("OK")
        except IOError:
            print("Error reading configuration file. Exiting...")
            exit(1)

        print("Initializing pygame...", end=" ")
        pygame.init()
        self.spritesList = pygame.sprite.Group()

        print("OK")
        print("Initializing screen, params: " + str(self.config["window"]) + "...", end=" ")

        # Vertical rotation is unsupported due to UI layout
        if self.config["window"]["height"] > self.config["window"]["width"]:
            print("The screen cannot be in a vertical orientation. Exiting...")
            exit(1)

        self.screen = Screen(self, self.config["window"])
        print("OK")

        self.mapDataFolder = path.dirname("../data/mapdata/")
        self.map = Map(path.join(self.mapDataFolder, 'map.txt'), self.screen)
        self.player = Player((6, 2), self.map.tileSize)
        self.map.addEntity(self.player)
        self.eventManager = EventManager(self, self.player)


        self.mainLoop()

    def mainLoop(self):
        while self.running:
            self.eventManager.handleEvents()
            self.spritesList.draw(self.screen.pygameScreen)
            pygame.display.flip()
