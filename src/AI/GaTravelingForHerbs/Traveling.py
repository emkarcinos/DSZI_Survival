from random import randint, sample
from math import sqrt

from src.AI.GaTravelingForHerbs.GeneticAlgorithm import GeneticAlgorithm

START_COORD = [(6, 2)]
END_COORD = [(10, 7)]
COORDS = [(12, 2), (16, 2), (17, 5), (14, 7), (17, 17), (13, 17), (5, 15), (2, 9), (8, 5), (11, 10)]


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

    def crossover(self, element2: 'Element') -> 'Element':
        childCoords = self.coords[1:int(len(self.coords) / 2)]
        for coord in element2.coords:
            if coord not in childCoords and coord not in END_COORD + START_COORD:
                childCoords.append(coord)

            if len(childCoords) == len(element2.coords):
                break
        return Traveling(START_COORD + childCoords + END_COORD)

    def mutation(self):
        first = randint(1, len(self.coords) - 2)
        second = randint(1, len(self.coords) - 2)
        self.coords[first], self.coords[second] = self.coords[second], self.coords[first]
        self.fitness = self.evaluate()

    def __repr__(self):
        return str(self.coords)


firstGeneration = [Traveling(START_COORD + sample(COORDS, len(COORDS)) + END_COORD) for _ in range(100)]
mutationProbability = float(0.1)

ga = GeneticAlgorithm(firstGeneration, mutationProbability)
movementList = ga.run()

