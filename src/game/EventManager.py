import pygame

from src.entities.Player import Rotations

# Player can move every given milliseconds
TIMEOUT = 100
class EventManager:
    keyTimeout = 0

    def __init__(self, gameObject, player):
        self.game = gameObject
        self.player = player
        self.keyTimer = pygame.time.Clock()
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
        self.keyTimeout += self.keyTimer.tick()
        if self.keyTimeout >= TIMEOUT:
            self.handlePlayerControls(keys)
            self.keyTimeout = 0

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

