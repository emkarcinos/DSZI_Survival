from random import random, choice

class GeneticAlgorithm:
    def __init__(self, firstPopulation, mutationProbability):
        self.firstPopulation = firstPopulation
        self.mutationProbability = mutationProbability

    def selectionModel(self, generation):
        max_selected = int(len(generation) / 10)
        sorted_by_assess = sorted(generation, key=lambda x: x.fitness)
        return sorted_by_assess[:max_selected]

    def stopCondition(self, i):
        return i == 100

    def run(self):
        population = self.firstPopulation
        population.sort(key=lambda x: x.fitness)
        populationLen = len(population)
        i = 0
        while True:
            selected = self.selectionModel(population)
            newPopulation = selected.copy()
            while len(newPopulation) != populationLen:
                child = choice(population).crossover(choice(population))
                if random() <= self.mutationProbability:
                    child.mutation()
                newPopulation.append(child)

            population = newPopulation
            theBestMatch = min(population, key=lambda x: x.fitness)
            print("Generation: {} S: {} fitness: {}".format(i, theBestMatch, theBestMatch.fitness))

            i += 1
            if self.stopCondition(i):
                return str(theBestMatch)


    def listOfTravel(self):
        strTravel = self.run()
        import ast
        return ast.literal_eval(strTravel)


