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
