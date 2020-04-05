from src.entities.Interactable import Interactable


class Npc(Interactable):
    def __init__(self, texture, pos, id, path, speed):
        Interactable.__init__(self, texture, pos, id)
        self.path = path
        self.speed = speed
