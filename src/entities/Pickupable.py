from src.entities import Statistics, Player
from src.entities.Interactable import Interactable


class Pickupable(Interactable):
    def __init__(self, texture, size, pos, Statistics):
        super().__init__(texture, size, pos)
        self.is_pickupable = True
        self.Statistics = Statistics

    def on_pickup(self, Player):
        Player.statistics.set_hp(self.Statistics.hp)
        Player.statistics.set_stamina(self.Statistics.stamina)
        Player.statistics.set_thirst(self.Statistics.thirst)
        Player.statistics.set_hunger(self.Statistics.hunger)

