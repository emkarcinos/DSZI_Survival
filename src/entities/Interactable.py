from src.entities.Entity import Entity
from src.entities.Enums import Classifiers


class Interactable(Entity):
    def __init__(self, texture, size, pos, Statistics, classifier=None):
        """
        Create an interactable entity, that can be interacted with.

        :param texture: Path to a file with the texture
        :param size: Size in px
        :param pos: A tuple of coords (x,y)
        :param Statistics: Outcome of the interaction
        :param classifier: Type of the entity (food, water, rest) as string
        """
        super().__init__(texture, size, pos)
        self.Statistics = Statistics

        self.classifier = None
        self.setClassifier(classifier)

    def setClassifier(self, classifier):
        if classifier == "food":
            self.classifier = Classifiers.FOOD
        elif classifier == "water":
            self.classifier = Classifiers.WATER
        elif classifier == "rest":
            self.classifier = Classifiers.REST
        elif classifier == "herb":
            self.classifier = Classifiers.HERB

    def on_interaction(self, Player):
        """
        Applies outcome to the Player

        :param Player: Player object
        """
        Player.statistics.set_hp(self.Statistics.hp)
        Player.statistics.set_stamina(self.Statistics.stamina)
        Player.statistics.set_thirst(self.Statistics.thirst)
        Player.statistics.set_hunger(self.Statistics.hunger)

        if self.classifier == Classifiers.HERB:
            Player.herbs += 1
            print(Player.herbs)

        if Player.herbs == 10:
            Player.statistics.set_hp(100)
            Player.statistics.set_stamina(100)
            Player.statistics.set_thirst(0)
            Player.statistics.set_hunger(0)

    def __str__(self):
        return "Entity - ID:{}, pos:({}x, {}y), {}".format(self.id, self.x, self.y, self.classifier.name)
