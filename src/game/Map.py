import pygame
from game.TerrainTile import TerrainTile
from game.Screen import Locations

class Map:
    def __init__(self, filename, game, screen):
        self.game = game
        self.screen = screen
        self.terrain = []
        self.entities = []
        with open(filename, 'rt') as f:
            for line in f:
                self.terrain.append(line)

        self.tileSize = self.screen.mapSize/20

        self.tileWidth = len(self.terrain[0])
        self.tileHeight = len(self.terrain)
        self.width = self.tileWidth * self.tileSize
        self.height = self.tileHeight * self.tileSize

        self.terrainDraw()
        
    def terrainDraw(self):
        for row, tiles in enumerate(self.terrain):
            for col, tile in enumerate(tiles):
                if tile == 'w':
                    self.screen.draw(TerrainTile(self.game, col, row, 'wall.png', self.screen.mapSize), Locations.MAP, col, row)
                if tile == ',':
                    self.screen.draw(TerrainTile(self.game, col, row, 'floor.png', self.screen.mapSize), Locations.MAP, col, row)
                if tile == '.':
                    self.screen.draw(TerrainTile(self.game, col, row, 'grass.png', self.screen.mapSize), Locations.MAP, col, row)
        

