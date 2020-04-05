import pygame
from game.TerrainTile import TerrainTile
from game.Screen import Locations

class Map:
    def __init__(self, filename, screen):
        self.screen = screen
        self.terrain = []
        self.collidableTerrain = []
        self.collidables = pygame.sprite.Group()

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
                if tile == 's':
                    self.screen.draw(TerrainTile(col, row, 'sand.png', self.tileSize), Locations.MAP, 0, 0)
                elif tile == ',':
                    self.screen.draw(TerrainTile(col, row, 'floor.png', self.tileSize), Locations.MAP, 0, 0)
                elif tile == '.':
                    self.screen.draw(TerrainTile(col, row, 'grass.png', self.tileSize), Locations.MAP, 0, 0)
                elif tile == 'x':
                    object = TerrainTile(col, row, 'water.jpg', self.tileSize)
                    self.screen.draw(object, Locations.MAP, 0, 0)
                    self.collidables.add(object)
                elif tile == 'w':
                    object = TerrainTile(col, row, 'wall.png', self.tileSize)
                    self.screen.draw(object, Locations.MAP, 0, 0)
                    self.collidables.add(object)

    def addEntity(self, entity):
        self.screen.draw(entity, Locations.MAP, 0, 0)
        self.collidables.add(entity)

    def removeSpriteFromMap(self, entity):
        if self.collidables.has(entity):
            self.collidables.remove(entity)
        self.screen.removeSprite(entity)

    # add object to map.collidables list to be collidable
    def collision(self, x, y):
        for b in self.collidables:
            if b.rect.x == x and b.rect.y == y:
                return True
        return False