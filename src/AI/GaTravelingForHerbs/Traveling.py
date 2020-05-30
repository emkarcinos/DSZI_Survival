from random import randint, sample
from math import sqrt

START_COORD = [(6, 2)]
END_COORD = [(10, 7)]


class Traveling:
    def __init__(self, coords):
        self.coords = coords
        self.fitness = self.evaluate()

    def evaluate(self):
        sum = 0
        for i, c in enumerate(self.coords):
            if i + 1 > len(self.coords) - 1:
                break
            nextCoord = self.coords[i + 1]
            # calculate distance
            sum += sqrt((nextCoord[0] - c[0]) ** 2 + (nextCoord[1] - c[1]) ** 2)
        return sum

    def crossover(self, parentCoords):
        childCoords = self.coords[1:int(len(self.coords) / 2)]
        for coord in parentCoords.coords:
            if coord not in childCoords and coord not in END_COORD + START_COORD:
                childCoords.append(coord)

            if len(childCoords) == len(parentCoords.coords):
                break
        return Traveling(START_COORD + childCoords + END_COORD)

    def mutation(self):
        first = randint(1, len(self.coords) - 2)
        second = randint(1, len(self.coords) - 2)
        self.coords[first], self.coords[second] = self.coords[second], self.coords[first]
        self.fitness = self.evaluate()

    def __repr__(self):
        return str(self.coords)
