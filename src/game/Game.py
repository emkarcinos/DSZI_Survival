import json
from os import path
from pathlib import Path
import os

import pygame

from src.AI.Affinities import Affinities
from src.AI.DecisionTrees.DecisionTree import DecisionTree
from src.AI.DecisionTrees.ExamplesManager import ExamplesManager
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalClassification import SurvivalClassification
from src.AI.GA import geneticAlgorithm
from src.entities.Player import Player
from src.game.EventManager import EventManager
from src.game.Map import Map
from src.game.Screen import Screen
from src.game.Timer import Timer
import src.AI.DecisionTrees.InductiveDecisionTreeLearning as DT
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalAttributesDefinitions import \
    SurvivalAttributesDefinitions as AttrDefs
from src.AI.SurvivalDT import SurvivalDT
from src.AI.GA_With_DT import geneticAlgorithmWithDecisionTree


# Main Game class
class Game:
    def __init__(self, filesPath, argv):
        """
        Game script initialization. Loads all files, creates screen, map, tiles, entities and a player.
        Starts the main game loop at the end.

        :param filesPath: Absolute path to the root of the gamefiles
        :param argv: Runnable arguments
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
        if len(argv) < 2:
            print("No arguments specified.")
            exit(1)
        elif argv[1] == "test":
            self.testRun(filesPath)
        # Decision tree
        elif argv[1] == "dt":
            if len(argv) >= 3:
                if argv[2] == "-p":
                    print("Running Decision Tree in pause mode.")
                    self.dtRun(filesPath, True)
                else:
                    print("Running Decision Tree.")
                    self.dtRun(filesPath)
            else:
                print("Running Decision Tree.")
                self.dtRun(filesPath)
        # Genetic algorithm
        elif argv[1] == "ga" and len(argv) >= 3:
            if len(argv) >= 4 and argv[3] == "-t":
                print("Running Genetic Algorithm in multithreaded mode, iter = ", argv[2])
                self.gaRun(filesPath, int(argv[2]), multithread=True)
            else:
                print("Running Genetic Algorithm in singlethreaded mode, iter = ", argv[2])
                self.gaRun(filesPath, int(argv[2]))
        # Genetic algorithm with decision tree
        elif argv[1] == "ga_dt" and len(argv) >= 3:
            print("Running Genetic Algorithm with Decision Tree, iter = ", argv[2])
            self.gaDTRun(filesPath, int(argv[2]))
        # Generating examples for decision tree
        elif argv[1] == "g_e_dt":
            print("Running in mode generating examples for decision tree.")
            examplesFilePath = str(filesPath) + os.sep + "data" + os.sep + "AI_data" + os.sep + "dt_exmpls" + os.sep + "dt_examples"
            dtExampleManager = ExamplesManager(examplesFilePath)
            dtExampleManager.generateExamples()
        # Invalid game mode
        else:
            print("Invalid game mode. \n Possible options: test, ga")
            exit(1)

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
        self.player = Player((6, 2), self.map.tileSize, Affinities(0.3, 0.6, 0.1, 0.5))
        self.map.addEntity(self.player, DONTADD=True)
        self.eventManager = EventManager(self, self.player)

        # Start game loop
        self.mainLoop()

    def gaRun(self, filesPath, iter, multithread=False):
        """
        Runs the game in GA mode - runs genetic algorithm in headless mode.

        :param filesPath: Absolute path to game's root directory
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

        # Run GA:
        self.pgTimer.tick()
        geneticAlgorithm(self.map, iter, 10, 0.1, multithread)
        print("Time elapsed: ", self.pgTimer.tick() // 1000)

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

    def dtRun(self, filesPath, pauseAfterDecision=False):
        """
        Runs game in decision tree mode.

        In this mode user can only watch how player performs decisions with usage of decision tree.

        :param pauseAfterDecision: If pause mode is true, then simulation will be paused after each tree decision.
        :param filesPath:
        """
        self.running = True
        print("Initializing screen, params: " + str(self.config["window"]) + "...", end=" ")

        # Vertical rotation is unsupported due to UI layout
        if self.config["window"]["height"] > self.config["window"]["width"]:
            print("The screen cannot be in a vertical orientation. Exiting...")
            exit(1)

        # Read examples to decision tree learning
        examplesFilePath = str(
            filesPath) + os.sep + "data" + os.sep + "AI_data" + os.sep + "dt_exmpls" + os.sep + "dt_examples"
        examplesManager = ExamplesManager(examplesFilePath)
        examples = examplesManager.readExamples()

        # Create decision tree
        survivalDecisionTree = SurvivalDT(DT.inductiveDecisionTreeLearning(examples,
                                                                           AttrDefs.allAttributesDefinitions,
                                                                           SurvivalClassification.FOOD,
                                                                           SurvivalClassification))

        print("\nDecision tree: \n")
        DecisionTree.printTree(survivalDecisionTree.entityPickingDecisionTree, 0)
        print()

        # Initialize timers
        # Virtual timer to track in-game time
        self.ingameTimer = Timer()
        self.ingameTimer.startClock()

        # Initialize screen
        self.screen = Screen(self, self.config["window"])
        print("OK")

        self.initializeMap(filesPath)

        # Initialize the player
        self.player = Player((6, 2), self.map.tileSize, Affinities(0.3, 0.6, 0.1, 0.5))
        self.map.addEntity(self.player, DONTADD=True)

        pause = False
        decisionsMade = 0

        # main loop without user input
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = not pause

            if pause or not self.running:
                pass

            else:
                # Tick the timers
                self.ingameTimer.updateTime(self.pgTimer.tick())
                self.screen.ui.updateTime()

                # If player is dead write information to console and break main loop
                if not self.player.alive:
                    self.screen.ui.updateOnDeath(self.player)
                    self.screen.ui.console.printToConsole("Score: {}".format(str(decisionsMade + self.player.movePoints)))
                    self.screen.ui.console.printToConsole("Decisions made {}. Movements made {}.".
                                                          format(decisionsMade, self.player.movePoints))
                    self.spritesList.update()
                    self.spritesList.draw(self.screen.pygameScreen)
                    pygame.display.flip()
                    self.running = False

                # Choose target for player using decision tree
                if self.player.movementTarget is None:
                    self.player.gotoToTarget(survivalDecisionTree.pickEntity(self.player, self.map), self.map)
                    decisionsMade += 1
                    if pauseAfterDecision:
                        pause = True

                self.screen.ui.updateBarsBasedOnPlayerStats(self.player.statistics)

                # Call update() method for each entity
                self.spritesList.update()

                # Draw all sprites
                self.spritesList.draw(self.screen.pygameScreen)

                # Flip the display
                pygame.display.flip()

    def gaDTRun(self, filesPath, iter):
        """
        Runs the game in GA with Decision Tree mode.

        :param filesPath: Absolute path to game's root directory
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

        # Run GA:
        self.pgTimer.tick()

        examplesFilePath = str(
            filesPath) + os.sep + "data" + os.sep + "AI_data" + os.sep + "dt_exmpls" + os.sep + "dt_examples"
        dtExamplesManager = ExamplesManager(examplesFilePath)
        dtExamples = dtExamplesManager.readExamples()

        geneticAlgorithmWithDecisionTree(self.map, iter, 10, dtExamples, 0.1)
        print("Time elapsed: ", self.pgTimer.tick() // 1000)

