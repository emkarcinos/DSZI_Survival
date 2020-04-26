import pygame
import json
from pathlib import Path
from os import path

from src.AI.AutomaticMovement import AutomaticMovement
from src.game.EventManager import EventManager
from src.game.Screen import Screen, Locations
from src.game.Map import Map

from src.entities.Player import Player
from src.game.Timer import Timer


class Game:
    def __init__(self, filesPath):
        self.running = True
        print("Loading configuration...", end=" ")

        try:
            configFolder = Path(str(filesPath) + "/data/config/")
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

        # Initialize timers
        self.pgTimer = pygame.time.Clock()
        self.ingameTimer = Timer()
        self.ingameTimer.startClock()

        self.deltaTime = 0
        self.lastTimePassed = self.ingameTimer.timePassed

        self.moveTimer = 0
        self.moveTime = 300


        self.screen = Screen(self, self.config["window"])
        print("OK")

        mapFile = Path(str(filesPath) + "/data/mapdata/")
        self.map = Map(path.join(mapFile, 'map.txt'), self.screen)
        self.player = Player((6, 2), self.map.tileSize)
        self.map.addEntity(self.player, DONTADD=True)
        self.eventManager = EventManager(self, self.player)

        self.movement = AutomaticMovement(self.player, self.map, self.screen.getUiWidth(Locations.LEFT_UI))


        testTarget = self.map.entities[0]
        if testTarget is self.player:
            testTarget = self.map.entities[1]

        self.movement.gotoToTarget(testTarget)

        self.mainLoop()

    def mainLoop(self):
        while self.running:
            # Update ingame clock
            self.ingameTimer.updateTime(self.pgTimer.tick())

            self.deltaTime = self.ingameTimer.timePassed - self.lastTimePassed
            self.lastTimePassed = self.ingameTimer.timePassed

            self.spritesList.update()
            self.eventManager.handleEvents()

            if self.moveTimer > 0:
                self.moveTimer -= self.deltaTime
            else:
                self.movement.updatePlayerCoords()
                self.moveTimer = self.moveTime
            self.spritesList.draw(self.screen.pygameScreen)
            pygame.display.flip()
