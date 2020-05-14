from pathlib import Path

import pygame

# TODO: Add getters to retrieve relative coords
from entities.Enums import Rotations, Movement


class Entity(pygame.sprite.Sprite):
    # Static ID counter - increments with each constructor call
    nextId = 1

    pygameTimer = pygame.time.Clock()

    def __init__(self, texture, size, pos):
        """
        Create an entity.
        :param texture: Path to a file with texture
        :param size: Size in px
        :param pos: Position tuple
        """
        super().__init__()
        self.image, self.rect = self.getTexture(texture, size)
        self.image.set_colorkey((255, 255, 255))
        # Relative coords
        self.x = pos[0]
        self.y = pos[1]
        # Rect has entities' absolute coords
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        # Unique ID
        self.id = self.setNewId()

        # Where the entity is facing
        self.rotation = Rotations.NORTH

        # Entity can move itself if this list has movements inside
        self.movesList = []
        self.movementTarget = None

        # How fast can en entity move
        self.moveTimeout = 100
        # Tracks time between every move
        self.movementTimer = 0

    # Setters and getters for coords
    def getCoords(self, screenRelative=False):
        if screenRelative:
            return self.rect.x, self.rect.y
        else:
            return self.x, self.y

    def setCoords(self, coords, screenRelative=False):
        if screenRelative:
            self.rect.x, self.rect.y = coords
        else:
            self.x, self.y = coords
            self.rect.x = coords[0] * self.rect.w  # TODO: Add screen offset
            self.rect.y = coords[1] * self.rect.h  # TODO: Add screen offset

    @staticmethod
    def setNewId():
        """
        Returns auto-incremented unique ID
        :return: ID Int
        """
        id = Entity.nextId
        Entity.nextId += 1
        return id

    @staticmethod
    def getTexture(textureName, tileSize):
        """
        Get the texture from a file. Texture path is pre-set to data/images/entities.
        :param textureName: Filename
        :param tileSize: Texture size (to scale to map size)
        :return: image, rect
        :rtype: pygame.image, pygame.rect
        """
        texturesFolder = ""
        textureFile = ""
        try:
            texturesFolder = Path("./data/images/entities")
            textureFile = texturesFolder / textureName
        except IOError:
            print("Cannot load texture from " + texturesFolder + ". Exiting...")
            exit(1)
        image = pygame.image.load(str(textureFile.resolve())).convert_alpha()
        image = pygame.transform.scale(image, (tileSize, tileSize))
        rect = image.get_rect()
        return image, rect

    def getFacingCoord(self):
        """
        Get coordinates forward to the player.
        :return: Position tuple
        """
        if self.rotation.value == Rotations.NORTH.value:
            return self.rect.x, self.rect.y - self.rect.h
        elif self.rotation.value == Rotations.SOUTH.value:
            return self.rect.x, self.rect.y + self.rect.h
        elif self.rotation.value == Rotations.EAST.value:
            return self.rect.x + self.rect.h, self.rect.y
        elif self.rotation.value == Rotations.WEST.value:
            return self.rect.x - self.rect.h, self.rect.y

    def move(self, movement):
        """
        This function will attempt to move an entity. It fails if the movement can not be done.
        :type movement: entities.Enums.Movement
        :param movement: specify what movement should be done (See Movement enum)
        :return: Returns true, if the movement has succeeded
        """
        # Can move if timeout has elapsed
        if self.movementTimer > self.moveTimeout:
            self.movementTimer = 0
            # Rotation
            if movement.value != Movement.FORWARD.value:
                self.updateRotation(movement)
            # Else move
            else:
                self.moveForward()
            return True
        else:
            return False

    # Deprecated - use move() instead
    def moveForward(self):
        """
        Moves the player forward. NOTE: should not be used outside of the player class.
        """
        # TODO: Use relative coords
        if self.rotation.value == Rotations.NORTH.value:
            self.rect.y -= self.rect.w
        elif self.rotation.value == Rotations.EAST.value:
            self.rect.x += self.rect.w
        elif self.rotation.value == Rotations.SOUTH.value:
            self.rect.y += self.rect.w
        elif self.rotation.value == Rotations.WEST.value:
            self.rect.x -= self.rect.w

    def updateRotation(self, movement):
        """
        A method that rotates an entity.
        :type movement: Movement
        :param movement: Rotation direction
        """
        if movement == Movement.ROTATE_L:
            self.rotate(Rotations((self.rotation.value - 1) % 4))
        elif movement == Movement.ROTATE_R:
            self.rotate(Rotations((self.rotation.value + 1) % 4))

    def rotate(self, rotation):
        """
        More low-level method than rotate - rotates the texture and updates the entity
        rotation field.
        :type rotation: Movement
        :param rotation:
        """
        # If the player is not facing given direction, it will not move the first time, it will only get rotated
        if self.rotation.value != rotation.value:
            self.image = pygame.transform.rotate(self.image, ((self.rotation.value - rotation.value) * 90))
            self.rotation = rotation

    def gotoToTarget(self, target, map):
        """
        Attempt to find a path to a given target. If the path is found, move to the target.
        :param target: Target object
        :param map: Map object
        """
        if self.movementTarget is None:
            self.movementTarget = target
            from AI.AutomaticMovement import aStar
            self.movesList = aStar(self, self.movementTarget, map)
            if not self.movesList:
                self.movementTarget = None

    def updateEntityCoords(self):
        """
        Called each frame. Will consume moves from the moveList, if there are any.
        """
        if self.movementTarget is not None and self.movesList:
            nextMove = self.movesList[0]
            if self.move(nextMove):
                self.movesList.remove(nextMove)
                if not self.movesList:
                    # Attempt to interact with the target.
                    try:
                        self.movementTarget.on_interaction(self)
                    except AttributeError:
                        pass
                    self.movementTarget = None

    def update(self):
        """
        Called every frame
        """
        # Add time elapsed between previous frame
        self.movementTimer += self.pygameTimer.tick()
        # If A* has ben called, move the entity
        self.updateEntityCoords()
