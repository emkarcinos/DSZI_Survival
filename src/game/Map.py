import json

import pygame

from src.entities.Interactable import Interactable
from src.game.TerrainTile import TerrainTile
from src.game.Screen import Locations

from src.entities.Entity import Entity
from src.entities.Pickupable import Pickupable
from src.entities.Statistics import Statistics


class Map:
    def __init__(self, filename, screen):
        self.screen = screen
        # tekstowa macierz terenów
        self.terrain = []
        # tereny bez kolizji
        self.terrainTilesList = []
        # grupa objektów kolizyjnych (tereny kolizyjne i entities)
        self.collidables = pygame.sprite.Group()
        # lista wszystkich entity
        self.entities = []

        with open(filename, 'rt') as f:
            for line in f:
                self.terrain.append(line)

        self.tileSize = int(self.screen.mapSize/20)

        self.tileWidth = len(self.terrain[0])
        self.tileHeight = len(self.terrain)
        self.width = self.tileWidth * self.tileSize
        self.height = self.tileHeight * self.tileSize

        self.terrainDraw()

        for entity in self.loadEntities(filename):
            self.addEntity(entity)

    # Returns a list of entities loaded from mapfile
    def loadEntities(self, mapFileName):
        mapFile = mapFileName.split('.txt')[0]
        entitiesFilePath = mapFile + "Entities.json"
        actualEntities = []
        with open(entitiesFilePath, 'rt') as file:
            entityListJson = json.loads(file.read())
            for entity in entityListJson:
                try:
                    # Creates a pickupable object
                    if entity["isPickupable"]:
                        actualEntities.append(Pickupable(entity["name"] + ".png",
                                                         self.tileSize,
                                                         (entity["position"]["x"] * self.tileSize, entity["position"]["y"] * self.tileSize),
                                                         Statistics(entity["effect"]["hp"],
                                                                    entity["effect"]["hunger"],
                                                                    entity["effect"]["thirst"],
                                                                    entity["effect"]["stamina"])))
                    # Creates an interactable object
                    elif "effect" in entity:
                        actualEntities.append(Interactable(entity["name"] + ".png",
                                                         self.tileSize,
                                                         (entity["position"]["x"] * self.tileSize,
                                                          entity["position"]["y"] * self.tileSize),
                                                         Statistics(entity["effect"]["hp"],
                                                                    entity["effect"]["hunger"],
                                                                    entity["effect"]["thirst"],
                                                                    entity["effect"]["stamina"])))
                    # Creates plain entity
                    else:
                        actualEntities.append(Entity(entity["name"] + ".png",
                                                        self.tileSize,
                                                        (entity["position"]["x"] * self.tileSize, entity["position"]["y"] * self.tileSize)))
                except KeyError:
                    print("Failed to load entity " + entity)
        return actualEntities

    def terrainDraw(self):
        for row, tiles in enumerate(self.terrain):
            for col, tile in enumerate(tiles):
                if tile == 's':
                    object = TerrainTile(col, row, 'sand.png', self.tileSize, 15)
                    self.screen.draw(object, Locations.MAP, 0, 0)
                    self.terrainTilesList.append(object)
                elif tile == ',':
                    object = TerrainTile(col, row, 'floor.png', self.tileSize, 0)
                    self.screen.draw(object, Locations.MAP, 0, 0)
                    self.terrainTilesList.append(object)
                elif tile == '.':
                    object = TerrainTile(col, row, 'grass.png', self.tileSize, 10)
                    self.screen.draw(object, Locations.MAP, 0, 0)
                    self.terrainTilesList.append(object)
                elif tile == 'c':
                    object = TerrainTile(col, row, 'clay.png', self.tileSize, 20)
                    self.screen.draw(object, Locations.MAP, 0, 0)
                    self.terrainTilesList.append(object)
                elif tile == 'x':
                    object = TerrainTile(col, row, 'water.png', self.tileSize, 0)
                    self.screen.draw(object, Locations.MAP, 0, 0)
                    self.collidables.add(object)
                elif tile == 'w':
                    object = TerrainTile(col, row, 'wall.png', self.tileSize, 0)
                    self.screen.draw(object, Locations.MAP, 0, 0)
                    self.collidables.add(object)

    def getEntityOnCoord(self, coord):
        result = None
        for entity in self.entities:
            if entity.rect.x == coord[0] and entity.rect.y == coord[1]:
                result = entity
        return result

    # W przypadku podania kordynatów playera, powinno zwrócić teren na którym jest player
    def getTileOnCoord_old(self, coord):
        result = None
        for tile in self.terrainTilesList:
            if tile.rect.x == coord[0] and tile.rect.y == coord[1]:
                result = tile
        return result


    def getTileOnCoord(self, coord):
        result = None
        for tile in self.terrainTilesList:
            if tile.rect.collidepoint(coord[0], coord[1]):
                result = tile
                break
        return result

    # TODO: REMOVE DONT ADD
    def addEntity(self, entity, DONTADD=False):
        self.screen.draw(entity, Locations.MAP, 0, 0)
        # dodajemy bo wszystkie entity są kolizyjne
        self.collidables.add(entity)
        if not DONTADD:
            self.entities.append(entity)

    # Usuwa entity lub teren z mapy
    def removeSpriteFromMap(self, sprite):
        if self.collidables.has(sprite):
            self.collidables.remove(sprite)
        if sprite in self.entities:
            self.entities.remove(sprite)
        if sprite in self.terrainTilesList:
            self.terrainTilesList.remove(sprite)
        self.screen.removeSprite(sprite)



    # add object to map.collidables list to be collidable
    def collision(self, x, y):
        for b in self.collidables:
            if b.rect.x == x and b.rect.y == y:
                return True
        return False
