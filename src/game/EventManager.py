import pygame

from src.entities.Player import Rotations


class EventManager:
    def __init__(self, gameObject, player):
        self.game = gameObject
        self.player = player

        # Player controls

    # TODO
    def loadKeyboardSettings(self):
        pass

    def handleEvents(self):
        pygame.event.pump()

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

        self.handlePlayerControls(keys)

    def handlePlayerControls(self, keys):
        # Key names are temporary
        # TODO: Load key bindings from JSON
        if keys[pygame.K_w]:
            self.player.move(Rotations.NORTH)
        if keys[pygame.K_s]:
            self.player.move(Rotations.SOUTH)
        if keys[pygame.K_d]:
            self.player.move(Rotations.EAST)
        if keys[pygame.K_a]:
            self.player.move(Rotations.WEST)

