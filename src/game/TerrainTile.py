import pygame
import os
from os import path


class TerrainTile(pygame.sprite.Sprite):
    def __init__(self, x, y, texture, tileSize):
        super().__init__()
        self.imagesFolder = path.dirname("../data/images/")
        self.terrainFolder = path.join(self.imagesFolder, 'terrain')
        self.image = pygame.image.load(os.path.join(self.terrainFolder, texture)).convert()
        self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tileSize
        self.rect.y = y * tileSize
