from random import Random
from time import sleep

from src.AI.Affinities import pickWeightedAffinity
from src.AI.GA import pickEntity
from src.ui.UiConsole import UiConsole
import pygame

from src.entities.Enums import Movement, Classifiers


class EventManager:
    def __init__(self, gameObject, player):
        """
        Create a singleton EventManager to handle events like keyboard input.

        :param gameObject: Game object
        :param player: The player
        """
        # TODO: Is this really necessary?
        self.game = gameObject

        self.player = player

        # TODO: Make this not retarded
        self.turnOff = False

    # TODO
    def loadKeyboardSettings(self):
        pass

    def handleEvents(self):
        """
        Called every frame. Captures keyboard input, PyGame events, updates the time and UI.
        """
        pygame.event.pump()

        if self.turnOff:
            print(self.player.movePoints)
            sleep(1)
            exit(0)

        # TODO: Move to ui.update()
        self.game.screen.ui.updateTime()

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.handleClickingOnCollidablesAndTerrains(pos)
            # TODO: Move to ui.update()
            self.game.screen.ui.updateBasedOnPygameEvent(event)
        if self.player.alive:
            # TODO: Add A* here?
            self.handlePlayerControls(keys)
        else:
            self.game.screen.ui.updateOnDeath(self.player)
            self.turnOff = True

        # TODO: Move to ui.update()
        self.game.screen.ui.updateBarsBasedOnPlayerStats(self.player.statistics)

    def handleClickingOnCollidablesAndTerrains(self, pos):
        """
        Handles clicking on objects. Calls A* functions to move the player to the object that the mouse was
        pointing to.

        :param pos: Absolute object coords as a tuple of (x,y)
        """
        # get a list of all collidables that are under the mouse cursor
        clicked_collidables = [s for s in self.game.map.collidables if s.rect.collidepoint(pos)]

        if len(clicked_collidables) > 0:
            entity = Random().choice(clicked_collidables)
            UiConsole.printToConsole(str(entity))
            self.player.gotoToTarget(entity, self.game.map)
        else:
            # get a list of all terrains that are under the mouse cursor
            clicked_terrains = [tile for tile in self.game.map.terrainTilesList if tile.rect.collidepoint(pos)]
            if len(clicked_terrains) > 0:
                print("Terrains under clik:")
                for terrain in clicked_terrains:
                    print(terrain)
            else:
                print("NO TERRAIN FOUND UNDER CLICK")

    def handlePlayerControls(self, keys):
        """
        Handles player movement with the keyboard.

        :param keys: A list of pressed keys
        """
        # Key names are temporary
        # TODO: Load key bindings from JSON

        # Picking up items
        if keys[pygame.K_SPACE]:
            object = self.game.map.getEntityOnCoord(self.player.getFacingCoord())
            self.player.move(Movement.PICKUP, object)
        if keys[pygame.K_w]:
            if not self.game.map.collision(self.player.getFacingCoord()[0], self.player.getFacingCoord()[1]):
                self.player.move(Movement.FORWARD)
        if keys[pygame.K_a]:
            self.player.move(Movement.ROTATE_L)
        if keys[pygame.K_d]:
            self.player.move(Movement.ROTATE_R)

        if keys[pygame.K_o]:
            if self.player.movementTarget is None:
                target = pickEntity(self.player, self.game.map)
                self.player.gotoToTarget(target, self.game.map)

        if keys[pygame.K_r]:
            self.game.map.respawn()

        # Pick random target for A* algorithm
        if keys[pygame.K_u]:
            while True:
                try:
                    if self.player.movementTarget is None:
                        from src.entities.Interactable import Interactable
                        playerPickType = pickWeightedAffinity(self.player.affinities)
                        UiConsole.printToConsole("player picked" + str(playerPickType))
                        self.player.gotoToTarget(Random().choice(self.game.map.getInteractablesByClassifier(playerPickType)),
                                                 self.game.map)
                    break
                except IndexError:
                    pass
