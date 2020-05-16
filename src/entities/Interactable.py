from src.entities.Entity import Entity


class Interactable(Entity):
    def __init__(self, texture, size, pos, Statistics, classifier=None):
        """
        Create an interactable entity, that can be interacted with.

        :param texture: Path to a file with the texture
        :param size: Size in px
        :param pos: A tuple of coords (x,y)
        :param Statistics: Outcome of the interaction
        :param classifier: Type of the entity (food, water, rest)
        """
        super().__init__(texture, size, pos)
        self.Statistics = Statistics

        self.classifier = classifier

    def on_interaction(self, Player):
        """
        Applies outcome to the Player

        :param Player: Player object
        """
        Player.statistics.set_hp(self.Statistics.hp)
        Player.statistics.set_stamina(self.Statistics.stamina)
        Player.statistics.set_thirst(self.Statistics.thirst)
        Player.statistics.set_hunger(self.Statistics.hunger)

    def __str__(self):
        return "Entity - ID:{}, pos:({}x, {}y), {}".format(self.id, self.x, self.y, self.classifier)
