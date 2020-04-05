import pygame

from src.entities.Pickupable import Pickupable
from src.entities.Player import Rotations

# Player can move every given milliseconds
TIMEOUT = 100
class EventManager:
    keyTimeout = 0

    #self.game.map
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

        self.game.screen.ui.timerTextView.changeText(self.game.ingameTimer.getPrettyTime())

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            self.game.screen.ui.updateBasedOnPygameEvent(event)
        self.keyTimeout += self.keyTimer.tick()
        if self.keyTimeout >= TIMEOUT:
            self.handlePlayerControls(keys)
            self.keyTimeout = 0

        self.game.screen.ui.updateBasedOnPlayerStats(self.player.statistics)

    def handlePlayerControls(self, keys):
        # Key names are temporary
        # TODO: Load key bindings from JSON
        if keys[pygame.K_SPACE]:
            object = self.game.map.getEntityOnCoord(self.player.getFacingCoord())
            if type(object) is Pickupable:
                object.on_pickup(self.player)
                self.game.map.removeSpriteFromMap(object)
        if keys[pygame.K_w]:
            self.player.rotate(Rotations.NORTH)
            if not self.game.map.collision(self.player.rect.x, self.player.rect.y - self.player.rect.w):
                self.player.move(Rotations.NORTH)
        if keys[pygame.K_s]:
            self.player.rotate(Rotations.SOUTH)
            if not self.game.map.collision(self.player.rect.x, self.player.rect.y + self.player.rect.w):
                self.player.move(Rotations.SOUTH)
        if keys[pygame.K_d]:
            self.player.rotate(Rotations.EAST)
            if not self.game.map.collision(self.player.rect.x + self.player.rect.w, self.player.rect.y):
                self.player.move(Rotations.EAST)
        if keys[pygame.K_a]:
            self.player.rotate(Rotations.WEST)
            if not self.game.map.collision(self.player.rect.x - self.player.rect.w, self.player.rect.y):
                self.player.move(Rotations.WEST)



