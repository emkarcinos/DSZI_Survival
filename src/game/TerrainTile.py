from pathlib import Path

import pygame


# TODO: Relative coords
class TerrainTile(pygame.sprite.Sprite):
    def __init__(self, x, y, texture, tileSize, cost):
        """
        Create a tile object.

        :param x: Absolute X coord
        :param y: Absolute Y coord
        :param texture: Texture name found in data/images/terrain
        :param tileSize: Size in px
        :param cost: Cost of getting into this tile
        """
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

    def __repr__(self):
        coords = (self.x, self.y)
        return str(coords)
