import pygame
import os
from os import path


class TerrainTile(pygame.sprite.Sprite):
    def __init__(self, texture, tileSize):
        super().__init__()
        self.imagesFolder = path.dirname("../data/images/")
        self.terrainFolder = path.join(self.imagesFolder, 'terrain')
        self.image = pygame.image.load(os.path.join(self.terrainFolder, texture)).convert()
        self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
        self.rect = self.image.get_rect()
