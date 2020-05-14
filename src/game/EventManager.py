from random import Random
from time import sleep

import pygame

from src.entities.Enums import Movement


class EventManager:
    def __init__(self, gameObject, player):
        # TODO: Is this really necessary?
        self.game = gameObject

        self.player = player

        # TODO: Make this not retarded
        self.turnOff = False

    # TODO
    def loadKeyboardSettings(self):
        pass

    def handleEvents(self):
        pygame.event.pump()

        if self.turnOff:
            sleep(5)
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
        # get a list of all collidables that are under the mouse cursor
        clicked_collidables = [s for s in self.game.map.collidables if s.rect.collidepoint(pos)]

        if len(clicked_collidables) > 0:
            self.player.gotoToTarget(Random().choice(clicked_collidables), self.game.map)
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

        # Pick random target for A* algorithm
        if keys[pygame.K_u]:
            while True:
                try:
                    self.player.gotoToTarget(Random().choice(self.game.map.entities), self.game.map)
                    break
                except IndexError:
                    pass
