from src.entities.Entity import Entity


class Interactable(Entity):
    def __init__(self, texture, size, pos, Statistics):
        super().__init__(texture, size, pos)
        self.Statistics = Statistics

    def on_interaction(self, Player):
        Player.statistics.set_hp(self.Statistics.hp)
        Player.statistics.set_stamina(self.Statistics.stamina)
        Player.statistics.set_thirst(self.Statistics.thirst)
        Player.statistics.set_hunger(self.Statistics.hunger)

