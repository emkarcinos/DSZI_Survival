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


# Main Game class
class Game:
    def __init__(self, filesPath):
        self.running = True
        print("Loading configuration...", end=" ")

        # Load config params from file
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

        # Initialize screen
        self.screen = Screen(self, self.config["window"])
        print("OK")

        # Initialize timers
        # PyGame timer - precise timer, counts milliseconds every frame
        self.pgTimer = pygame.time.Clock()
        # Virtual timer to track in-game time
        self.ingameTimer = Timer()
        self.ingameTimer.startClock()

        self.deltaTime = 0
        self.lastTimePassed = self.ingameTimer.timePassed

        self.moveTimer = 0
        self.moveTime = 100

        # Load map data from file
        try:
            mapFile = Path(str(filesPath) + "/data/mapdata/")
        except IOError:
            print("Could not load map data. Exiting...")
            exit(1)

        # Initialize map object
        self.map = Map(path.join(mapFile, 'map.txt'), self.screen)

        # Initialize the player
        self.player = Player((6, 2), self.map.tileSize)
        self.map.addEntity(self.player, DONTADD=True)
        self.eventManager = EventManager(self, self.player)

        # A* algorithm
        self.movement = AutomaticMovement(self.player, self.map, self.screen.getUiWidth(Locations.LEFT_UI))

        testTarget = self.map.entities[0]
        if testTarget is self.player:
            testTarget = self.map.entities[1]

        self.movement.gotoToTarget(testTarget)

        # Start game loop
        self.mainLoop()

    def mainLoop(self):
        while self.running:
            # Tick the timers
            self.ingameTimer.updateTime(self.pgTimer.tick())

            self.deltaTime = self.ingameTimer.timePassed - self.lastTimePassed
            self.lastTimePassed = self.ingameTimer.timePassed

            # Handle all events
            self.eventManager.handleEvents()

            # Call update() method for each entity
            self.spritesList.update()

            if self.moveTimer > 0:
                self.moveTimer -= self.deltaTime
            else:
                self.movement.updatePlayerCoords()
                self.moveTimer = self.moveTime

            # Draw all sprites
            self.spritesList.draw(self.screen.pygameScreen)

            # Flip the display
            pygame.display.flip()
