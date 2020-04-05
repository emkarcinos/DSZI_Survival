from src.entities.Entity import Entity


class Interactable(Entity):

    def __init__(self, texture, pos, id):
        super().__init__(texture, pos, id)

    @staticmethod
    def interact_with_hp(hp, Statistics):
        Statistics.set_hp(hp)

    @staticmethod
    def interact_with_hunger(hunger, Statistics):
        Statistics.set_hunger(hunger)

    @staticmethod
    def interact_with_thirst(thirst, Statistics):
        Statistics.set_thirst(thirst)

    @staticmethod
    def interact_with_stamina(stamina, Statistics):
        Statistics.set_stamina(stamina)

