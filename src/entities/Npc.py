from src.entities.Collidable import Collidable
from src.entities.Interactable import Interactable


class Npc(Collidable, Interactable):
    def __init__(self, texture, pos, id, path, speed):
        Collidable.__init__(self, texture, pos, id)
        Interactable.__init__(self, texture, pos, id)
        self.path = path
        self.speed = speed
