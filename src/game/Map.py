import json

import pygame

from src.entities.Enums import Classifiers
from src.entities.Interactable import Interactable
from src.game.TerrainTile import TerrainTile
from src.game.Screen import Locations

from src.entities.Entity import Entity
from src.entities.Pickupable import Pickupable
from src.entities.Statistics import Statistics


class Map:
    def __init__(self, filename, screen):
        """
        Create a map object.

        :param filename: File name containing map data and JSON with entity data
        :param screen: Screen object
        """
        # TODO: Should map be self-aware of its own loacation?
        self.screen = screen

        # tekstowa macierz terenów
        self.terrain = []
        # tereny nie kolizyjne, potrzebne też do metody movableList, która zwraca tereny na których nie ma żadnych entity
        self.terrainTilesList = []
        # grupa objektów kolizyjnych (tereny kolizyjne i entities)
        self.collidables = pygame.sprite.Group()
        # lista wszystkich entity
        self.entities = pygame.sprite.Group()

        self.entitiesRawData = []

        self.filename = filename

        with open(self.filename, 'rt') as f:
            for line in f:
                self.terrain.append(line)

        self.tileSize = int(self.screen.mapSize/20)

        self.tileWidth = len(self.terrain[0])
        self.tileHeight = len(self.terrain)
        self.width = self.tileWidth * self.tileSize
        self.height = self.tileHeight * self.tileSize

        self.terrainDraw()

        for entity in self.loadEntities(self.filename):
            self.entitiesRawData.append(entity)
            self.addEntity(entity)

    def loadEntities(self, mapFileName):
        """
        Attempts to load all entities from mapdata JSON file.

        :param mapFileName: name of map file
        :return: list of loaded entities
        """
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
                                                         (entity["position"]["x"], entity["position"]["y"]),
                                                         Statistics(entity["effect"]["hp"],
                                                                    entity["effect"]["hunger"],
                                                                    entity["effect"]["thirst"],
                                                                    entity["effect"]["stamina"]),
                                                         entity["type"]))
                    # Creates an interactable object
                    elif "effect" in entity:
                        actualEntities.append(Interactable(entity["name"] + ".png",
                                                           self.tileSize,
                                                           (entity["position"]["x"], entity["position"]["y"]),
                                                           Statistics(entity["effect"]["hp"],
                                                                      entity["effect"]["hunger"],
                                                                      entity["effect"]["thirst"],
                                                                      entity["effect"]["stamina"]),
                                                           entity["type"]))
                    # Creates plain entity
                    else:
                        actualEntities.append(Entity(entity["name"] + ".png",
                                                     self.tileSize,
                                                     (entity["position"]["x"], entity["position"]["y"])))
                except KeyError:
                    print("Failed to load entity " + entity)
        return actualEntities

    def getInteractablesByClassifier(self, classifier=None):
        """
        Return a list of all Interactable entities by a given classifier.
        If the classifier is None, returns all interactables.

        :type classifier: Classifiers
        :param classifier: Classifier
        """
        result = []
        for entity in self.entities.sprites():
            if isinstance(entity, Interactable):
                if classifier is None:
                    result.append(entity)
                elif entity.classifier.value == classifier.value:
                    result.append(entity)
        return result

    def getEntitiesByType(self, type):
        """
        Get a list of all entities by their type.

        :param type: Entity type as class tpe
        :return A list of all entities of specified type
        """
        result = []
        for entity in self.entities.sprites():
            if isinstance(entity, type):
                result.append(entity)

        return result

    def terrainDraw(self):
        """
        Composes terrain data.

        """
        for row, tiles in enumerate(self.terrain):
            for col, tile in enumerate(tiles):
                if tile == 's':
                    object = TerrainTile(col, row, 'sand.png', self.tileSize, 15)
                    self.screen.addSprite(object, Locations.MAP)
                    self.terrainTilesList.append(object)
                elif tile == ',':
                    object = TerrainTile(col, row, 'floor.png', self.tileSize, 0)
                    self.screen.addSprite(object, Locations.MAP)
                    self.terrainTilesList.append(object)
                elif tile == '.':
                    object = TerrainTile(col, row, 'grass.png', self.tileSize, 10)
                    self.screen.addSprite(object, Locations.MAP)
                    self.terrainTilesList.append(object)
                elif tile == 'c':
                    object = TerrainTile(col, row, 'clay.png', self.tileSize, 20)
                    self.screen.addSprite(object, Locations.MAP)
                    self.terrainTilesList.append(object)
                elif tile == 'x':
                    object = TerrainTile(col, row, 'water.png', self.tileSize, 0)
                    self.screen.addSprite(object, Locations.MAP)
                    self.collidables.add(object)
                elif tile == 'w':
                    object = TerrainTile(col, row, 'wall.png', self.tileSize, 0)
                    self.screen.addSprite(object, Locations.MAP)
                    self.collidables.add(object)

    def respawn(self):
        """
        Respawns all entities on the map.
        """
        for entity in self.entities.sprites():
            entity.kill()

        for entity in self.entitiesRawData:
            self.addEntity(entity)

    def getEntityOnCoord(self, coord, screenRelative=False):
        """
        Get an entity on a given coordinate

        :param coord: Coords tuple of (x,y)
        :param screenRelative: True, if coords are screen-relative (default = False)
        :return: Entity
        """
        result = None
        for entity in self.entities:
            if screenRelative:
                if entity.rect.x == coord[0] and entity.rect.y == coord[1]:
                    result = entity
            else:
                if entity.x == coord[0] and entity.y == coord[1]:
                    result = entity
        return result

    def getTileOnCoord(self, coord, screenRelative=False):
        """
        Gets a tile object on a given coordinate.

        :param coord: A tuple of coords containing (x,y).
        :param screenRelative: Set to true, if the passed coords are absolute to the screen (default=False)
        :return: Tile object
        """
        result = None
        for tile in self.terrainTilesList:
            isColliding = False
            if screenRelative:
                isColliding = tile.rect.collidepoint(coord[0], coord[1])
            else:
                isColliding = tile.rect.collidepoint(coord[0] * self.tileSize + self.screen.mapCoord,
                                                     coord[1] * self.tileSize)
            if isColliding:
                result = tile
                break
        return result

    # TODO: REMOVE DONT ADD
    def addEntity(self, entity, DONTADD=False):
        """
        Adds an entity to the map.

        :param entity: Entity
        :param DONTADD: ????
        """
        self.screen.addSprite(entity, Locations.MAP)
        # dodajemy bo wszystkie entity są kolizyjne
        self.collidables.add(entity)
        if not DONTADD:
            self.entities.add(entity)

    def collision(self, x, y, screenRelative=False):
        """
        Check if a collision occurs on given coordinates.

        :param x: X coord
        :param y: Y coord
        :param screenRelative: Set this to true, if the passed coords are absolute (default = false)
        :return: True, if the collision happens.
        """
        if not screenRelative:
            for b in self.collidables:
                # Temp coord translation
                if b.rect.x == (x * self.tileSize + self.screen.mapCoord) and b.rect.y == y * self.tileSize:
                    return True
            return False
        else:
            for b in self.collidables:
                if b.rect.x == x and b.rect.y == y:
                    return True
            return False

    def insertHerbs(self, coordsList):
        nr = 1
        for i in range(10):
            entity = Pickupable("herb" + str(nr) + ".png", self.tileSize, coordsList[i], Statistics(0, 0, 0, 0), "herb")
            self.entitiesRawData.append(entity)
            self.addEntity(entity)
            nr += 1

    def movableList(self):
        terrainList = self.terrainTilesList
        for i in self.entities:
            terrainList.remove(self.getTileOnCoord((i.x, i.y)))
        return terrainList

    def __del__(self):
        for entity in self.entities.sprites():
            entity.kill()
            del entity
