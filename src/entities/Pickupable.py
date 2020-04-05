import src.entities.Interactable as Interactable
from src.entities import Statistics, Player
from game.MapNew import Map

class Pickupable(Interactable):
    def __init__(self, texture, pos, id, Statistics):
        super().__init__(texture, pos, id)
        self.is_pickupable = True
        self.Statistics = Statistics

    def on_pickup(self, Player):
        Player.statistics.set_hp(self.Statistics.hp)
        Player.statistics.set_stamina(self.Statistics.stamina)
        Player.statistics.set_thirst(self.Statistics.thirst)
        Player.statistics.set_hunger(self.Statistics.hunger)

        Map.removeSpriteFromMap(self)
