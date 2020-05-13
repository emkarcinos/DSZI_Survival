from src.entities.Interactable import Interactable


class Pickupable(Interactable):
    def __init__(self, texture, size, pos, Statistics):
        super().__init__(texture, size, pos, Statistics)
        self.is_pickupable = True

    def on_interaction(self, Player):
        super(Pickupable, self).on_interaction(Player)
        self.kill()
