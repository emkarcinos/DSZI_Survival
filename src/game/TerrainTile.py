from pathlib import Path

import pygame


class TerrainTile(pygame.sprite.Sprite):
    def __init__(self, x, y, texture, tileSize, cost):
        super().__init__()
        terrainTexturesPath = Path("./data/images/terrain").resolve()
        self.image = pygame.image.load(str(terrainTexturesPath / texture)).convert()
        self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tileSize
        self.rect.y = y * tileSize
        self.cost = cost

