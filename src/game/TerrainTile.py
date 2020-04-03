import pygame
import os
from os import path


class TerrainTile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, texture, mapSize):
        self.tiles = []
        self.groups = game.spritesList
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.imagesFolder = path.dirname("../data/images/")
        self.terrainFolder = path.join(self.imagesFolder, 'terrain')
        self.image = pygame.image.load(os.path.join(self.terrainFolder, texture)).convert()
        self.image.set_colorkey((0,100,0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.tileSize = mapSize/20
        self.rect.x = self.x * self.tileSize
        self.rect.y = self.y * self.tileSize
