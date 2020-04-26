from random import Random
from time import sleep

import pygame

from src.entities.Interactable import Interactable
from src.entities.Pickupable import Pickupable
from src.entities.Player import Movement

# Player can move every given milliseconds
TIMEOUT = 100
class EventManager:
    keyTimeout = 0

    #self.game.map
    def __init__(self, gameObject, player):
        self.game = gameObject
        self.player = player
        self.keyTimer = pygame.time.Clock()

        self.turnOff = False
        # Player controls

    # TODO
    def loadKeyboardSettings(self):
        pass

    def handleEvents(self):
        pygame.event.pump()

        if self.turnOff:
            sleep(5)
            exit(0)

        self.game.screen.ui.updateTime()

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # get a list of all sprites that are under the mouse cursor
                clicked_collidables = [s for s in self.game.map.collidables if s.rect.collidepoint(pos)]
                # do something with the clicked sprites...
                if len(clicked_collidables) > 0:
                    self.game.movement.gotoToTarget(Random().choice(clicked_collidables))
                else:
                    clicked_terrains = [tile for tile in self.game.map.terrainTilesList if tile.rect.collidepoint(pos)]
                    if len(clicked_terrains) > 0:
                        print("Terrains under clik:")
                        for terrain in clicked_terrains:
                            print(terrain)
                    else:
                        print("NO TERRAIN FOUND UNDER CLICK")

            self.game.screen.ui.updateBasedOnPygameEvent(event)
        self.keyTimeout += self.keyTimer.tick()
        if self.keyTimeout >= TIMEOUT:
            if self.player.alive:
                self.handlePlayerControls(keys)
                self.keyTimeout = 0
            else:
                self.game.screen.ui.updateOnDeath(self.player)
                self.turnOff = True

        self.game.screen.ui.updateBarsBasedOnPlayerStats(self.player.statistics)

    def handlePlayerControls(self, keys):
        # Key names are temporary
        # TODO: Load key bindings from JSON

        # Picking up items
        if keys[pygame.K_SPACE]:
            object = self.game.map.getEntityOnCoord(self.player.getFacingCoord())
            # Picked up item gets removed from the map
            if type(object) is Pickupable:
                object.on_interaction(self.player)
                self.game.screen.ui.updateOnPlayerPickup(self.player.statistics, object)
                self.game.map.removeSpriteFromMap(object)
            elif type(object) is Interactable:
                object.on_interaction(self.player)
                self.game.screen.ui.updateOnPlayerInteraction(self.player.statistics, object)

        # Movement
        # if keys[pygame.K_w]:
        #     self.player.rotate(Rotations.NORTH)
        #     if not self.game.map.collision(self.player.rect.x, self.player.rect.y - self.player.rect.w):
        #         self.player.move(Rotations.NORTH)
        # if keys[pygame.K_s]:
        #     self.player.rotate(Rotations.SOUTH)
        #     if not self.game.map.collision(self.player.rect.x, self.player.rect.y + self.player.rect.w):
        #         self.player.move(Rotations.SOUTH)
        # if keys[pygame.K_d]:
        #     self.player.rotate(Rotations.EAST)
        #     if not self.game.map.collision(self.player.rect.x + self.player.rect.w, self.player.rect.y):
        #         self.player.move(Rotations.EAST)
        # if keys[pygame.K_a]:
        #     self.player.rotate(Rotations.WEST)
        #     if not self.game.map.collision(self.player.rect.x - self.player.rect.w, self.player.rect.y):
        #         self.player.move(Rotations.WEST)
        if keys[pygame.K_w]:
            # TODO: Collision ckecks
            self.player.move(Movement.FORWARD)
        if keys[pygame.K_a]:
            self.player.move(Movement.ROTATE_L)
        if keys[pygame.K_d]:
            self.player.move(Movement.ROTATE_R)

        # Pick random target for A* algorithm
        if keys[pygame.K_u]:
            while True:
                try:
                    self.game.movement.gotoToTarget(Random().choice(self.game.map.entities))
                    break
                except IndexError:
                    pass


