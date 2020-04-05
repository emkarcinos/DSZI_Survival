import pygame
from game.TerrainTile import TerrainTile
from game.Screen import Locations

class Map:
    def __init__(self, filename, screen):
        self.screen = screen
        self.terrain = []
        self.entities = []
        self.collidableTerrain = []

        with open(filename, 'rt') as f:
            for line in f:
                self.terrain.append(line)

        self.tileSize = int(self.screen.mapSize/20)

        self.tileWidth = len(self.terrain[0])
        self.tileHeight = len(self.terrain)
        self.width = self.tileWidth * self.tileSize
        self.height = self.tileHeight * self.tileSize

        self.terrainDraw()

    def terrainDraw(self):
        for row, tiles in enumerate(self.terrain):
            for col, tile in enumerate(tiles):
                if tile == 'w':
                    self.screen.draw(TerrainTile('wall.png', self.tileSize), Locations.MAP, col*self.tileSize, row*self.tileSize)
                    self.collidableTerrain.append(self.terrain)
                elif tile == ',':
                    self.screen.draw(TerrainTile('floor.png', self.tileSize), Locations.MAP, col*self.tileSize, row*self.tileSize)
                elif tile == '.':
                    self.screen.draw(TerrainTile('grass.png', self.tileSize), Locations.MAP, col*self.tileSize, row*self.tileSize)

    def addEntity(self, entity):
        self.entities.append(entity)
        self.screen.draw(entity, Locations.MAP, 0, 0)

