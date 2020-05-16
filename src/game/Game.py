import json
from os import path
from pathlib import Path

import pygame

from src.AI.Affinities import Affinities
from src.entities.Player import Player
from src.game.EventManager import EventManager
from src.game.Map import Map
from src.game.Screen import Screen, Locations
from src.game.Timer import Timer


# Main Game class
class Game:
    def __init__(self, filesPath, gamemode="test"):
        """
        Game script initialization. Loads all files, creates screen, map, tiles, entities and a player.
        Starts the main game loop at the end.

        :param filesPath: Absolute path to the root of the gamefiles
        :param gamemode: Mode to run. Currently, there's only test gamemode.
        """

        # If set to true, gameloop will run
        self.running = False
        # Config dict
        self.config = None
        # Container for all sprites
        self.spritesList = None
        # PyGame timer
        self.pgTimer = None
        # Custom in-game timer
        self.ingameTimer = None
        # Screen object
        self.screen = None
        # Map object
        self.map = None
        # The player
        self.player = None
        # EventManager object
        self.eventManager = None

        self.loadConfig(filesPath)

        self.initializePygame()

        # Runnable selection
        if gamemode == "test":
            self.testRun(filesPath)

        # Start game loop
        self.mainLoop()

    def initializePygame(self):
        """
        Initializes all pygame members.

        """
        print("Initializing pygame...", end=" ")
        pygame.init()
        self.spritesList = pygame.sprite.Group()

        print("OK")

        # PyGame timer - precise timer, counts milliseconds every frame
        self.pgTimer = pygame.time.Clock()

    def initializeMap(self, filesPath):
        """
        Initializes the map object.

        :param filesPath:
        """
        mapFile = None
        try:
            mapFile = Path(str(filesPath) + "/data/mapdata/")
        except IOError:
            print("Could not load map data. Exiting...")
            exit(1)

        self.map = Map(path.join(mapFile, 'map.txt'), self.screen)

    def loadConfig(self, filesPath):
        """
        Loads the configuration file.

        :param filesPath: Absolute path to game folder
        """
        print("Loading configuration...", end=" ")
        try:
            configFolder = Path(str(filesPath) + "/data/config/")
            configFile = configFolder / "mainConfig.json"

            self.config = json.loads(configFile.read_text())

            print("OK")
        except IOError:
            print("Error reading configuration file. Exiting...")
            exit(1)

    def testRun(self, filesPath):
        """
        Run the game in test mode. In this mode, you can manually move the player and test the environment.

        :param filesPath: Absolute path to root game directory
        """
        self.running = True
        print("Initializing screen, params: " + str(self.config["window"]) + "...", end=" ")

        # Vertical rotation is unsupported due to UI layout
        if self.config["window"]["height"] > self.config["window"]["width"]:
            print("The screen cannot be in a vertical orientation. Exiting...")
            exit(1)

        # Initialize timers
        # Virtual timer to track in-game time
        self.ingameTimer = Timer()
        self.ingameTimer.startClock()

        # Initialize screen
        self.screen = Screen(self, self.config["window"])
        print("OK")

        self.initializeMap(filesPath)

        # Initialize the player
        self.player = Player((6, 2), self.map.tileSize, Affinities(0.3, 0.6, 0.1))
        self.map.addEntity(self.player, DONTADD=True)
        self.eventManager = EventManager(self, self.player)

    def mainLoop(self):
        """
        Continuously running loop. Calls events, updates and draws everything.
        """
        while self.running:
            # Tick the timers
            self.ingameTimer.updateTime(self.pgTimer.tick())

            # Handle all events
            self.eventManager.handleEvents()

            # Call update() method for each entity
            self.spritesList.update()

            # Draw all sprites
            self.spritesList.draw(self.screen.pygameScreen)

            # Flip the display
            pygame.display.flip()
