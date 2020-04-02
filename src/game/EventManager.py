import pygame


class EventManager:
    def __init__(self, gameObject):
        self.game = gameObject

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
