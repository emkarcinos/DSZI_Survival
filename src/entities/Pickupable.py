import src.entities.Interactable as Interactable
from src.entities import Statistics, Player


class Pickupable(Interactable):
    def __init__(self, texture, pos, id):
        super().__init__(texture, pos, id)
        self.is_pickupable = True

    def on_pickup(self, Player, Statistics):
        Player.statistics.set_hp(Statistics.hp)
        Player.statistics.set_stamina(Statistics.stamina)
        Player.statistics.set_thirst(Statistics.thirst)
        Player.statistics.set_hunger(Statistics.hunger)

        # TODO delete pickupable object from map
