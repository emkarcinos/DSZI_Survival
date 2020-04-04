from pathlib import Path
import pygame


class Entity:
    nextId = 1

    def __init__(self, texture, pos):
        self.image = texture
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.id = self.getId()

    # A method to return auto-incremented ID
    def getId(self):
        id = Entity.nextId
        Entity.nextId += 1
        return id

    # A method that returns image and rect from a file
    @staticmethod
    def getTexture(textureName, tileSize):
        texturesFolder = ""
        textureFile = ""
        try:
            texturesFolder = Path("../data/images/entities")
            textureFile = texturesFolder / textureName
        except IOError:
            print("Cannot load texture from " + texturesFolder + ". Exiting...")
            exit(1)
        image = pygame.image.load(str(textureFile)).convert_alpha()
        image = pygame.transform.scale(image, (tileSize, tileSize))
        rect = image.get_rect()
        return image, rect


