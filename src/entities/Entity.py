from pathlib import Path
import pygame


class Entity(pygame.sprite.Sprite):
    nextId = 1

    def __init__(self, texture, size, pos):
        super().__init__()
        self.image, self.rect = self.getTexture(texture, size)
        self.image.set_colorkey((255, 255, 255))
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.id = self.getId()

    # A method to return auto-incremented ID
    def getId(self):
        id = Entity.nextId
        Entity.nextId += 1
        return id

    # A method that returns image and rect from a file
    def getTexture(self, textureName, tileSize):
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


