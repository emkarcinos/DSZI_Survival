import random

from src.entities.Enums import Classifiers


class Affinities:
    def __init__(self, food, water, rest, walking):
        """
        Create a container of affinities. Affinities describe, what type of entities a player prioritizes.
        :param food: Food affinity
        :param water: Freshwater affinity
        :param rest: Firepit affinity
        :param walking: How distances determine choices
        """
        self.food = food
        self.water = water
        self.rest = rest
        self.walking = walking

    def getWeigths(self):
        """
        Get a list of all affinities except walking.

        :return: List of weights
        """
        return [self.food, self.water, self.rest]
