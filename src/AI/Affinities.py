import random

from src.entities.Enums import Classifiers


class Affinities:
    def __init__(self, food, water, rest):
        """
        Create a container of affinities. Affinities describe, what type of entities a player prioritizes.
        :param food: Food affinity
        :param water: Freshwater affinity
        :param rest: Firepit affinity
        """
        self.food = food
        self.water = water
        self.rest = rest

    def getWeigths(self):
        return [self.food, self.water, self.rest]



def pickWeightedAffinity(affinities: Affinities):
    population = [Classifiers.FOOD, Classifiers.WATER, Classifiers.REST]
    weights = affinities.getWeigths()

    return random.choices(population, weights)

