import random
from datetime import datetime

import numpy
import copy

from src.AI.Affinities import Affinities
from src.AI.ThreadedSimulation import ThreadedSimulation
from src.entities.Enums import Classifiers
from src.entities.Player import Player
from src.game.Map import Map


def geneticAlgorithm(map, iter, solutions, mutationAmount=0.05, multithread=False, threadCount=4):
    """
    This algorithm will attempt to find the best affinities for player's goal choices.

    :param map: Map with all entities
    :param iter: Generations count
    :param solutions: Solutions per generation
    :param mutationAmount: Mutation strength
    """
    # Based on 4 weights, that are affinities tied to the player
    weightsCount = 4

    # Initialize the first population with random values
    initialPopulation = numpy.random.uniform(low=0.0, high=1.0, size=(solutions, weightsCount))
    population = initialPopulation
    maps = []

    if multithread:
        # Create a map for each thread
        print("Creating a map for each thread...")
        for i in range(solutions):
            maps.append(Map(map.filename, map.screen))

    # Initialize log file
    with open("results.txt", "w+") as f:
        f.write("GA Results from " + str(datetime.now()))
        f.write("\n")

    for i in range(iter):
        print("\nRunning {} generation...".format(i + 1))
        fitness = []
        if not multithread:
            for player in population:
                fitness.append(doSimulation(player, map))
        else:
            threads = []
            for a in range(solutions):
                thread = ThreadedSimulation(a+1, a+1, population[a], maps[a])
                threads.append(thread)
                thread.start()
            for t in threads:
                t.join()
                fitness.append(t.getResult())

        parents = selectMatingPool(population, fitness, int(solutions / 2))

        print("Best fitness: {}".format(max(fitness)))
        offspring = mating(parents, solutions, mutationAmount)
        print("Best offspring: ", offspring[0])
        population = offspring

        # Add info to logfile
        with open("results.txt", "a") as f:
            f.write("Population: {}\n".format(i))
            f.write("Best fitness: {}\n".format(max(fitness)))
            f.write("Best offspring: " + str(offspring[0]))
            f.write("\n\n")


def selectMatingPool(population, fitness, count):
    """
    Pick best players from a population.

    :param population: Entire population pool
    :param fitness: Fitnesses coresponding to each player
    :param count: Selection count
    """
    result = []
    bestIdxs = []
    for i in range(count):
        bestIdx = (numpy.where(fitness == numpy.max(fitness)))[0][0]
        fitness[bestIdx] = 0
        bestIdxs.append(bestIdx)
    for id in bestIdxs:
        result.append(population[id])
    return result


def mating(parents, offspringCount, mutationAmount):
    """
    Generate an offspring from parents.

    :param parents: Array of parents weights
    :param offspringCount: Offspring count
    :param mutationAmount: How strong is the mutation of the genes
    :return: An array of new offspring
    """
    offspring = []
    for i in range(offspringCount):
        parent1 = i % len(parents)
        parent2 = (i + 1) % len(parents)
        offspring.append(crossover(parents[parent1], parents[parent2]))

    offspring = mutation(offspring, mutationAmount)
    return offspring


def crossover(genes1, genes2):
    """
    Apply a crossover between two genes.
    Currently, it calculates the median.

    :param genes1: An array of genes
    :param genes2: An array of genes
    :return: Array of resulted genes
    """
    result = []
    for gene1, gene2 in zip(genes1, genes2):
        result.append((gene1 + gene2) / 2)
    return result


def mutation(offspring, mutationAmount):
    for player in offspring:
        randomGeneIdx = random.randrange(0, len(player))
        player[randomGeneIdx] = player[randomGeneIdx] + random.uniform(-1.0, 1.0) * mutationAmount
    return offspring


def doSimulation(weights, map):
    """
    Runs the simulation. Returns fitness.

    :param weights: A list of weights for players.
    :param map: Map object
    """
    player = Player((6, 2), map.tileSize, Affinities(weights[0], weights[1], weights[2], weights[3]))
    player.disableMovementTime()
    while player.alive:
        if player.movementTarget is None:
            target = pickEntity(player, map)
            player.gotoToTarget(target, map)
        player.update()
    fitness = player.movePoints
    player.kill()
    del player
    map.respawn()
    return fitness


def pickEntity(player, map):
    """
    Select an entity to become the next goal for the player. The entity is determined by
    player's affinities and the distances between the player and entities.

    :param player: Player object
    :param map: Map object
    :type map: Map
    :type player: Player
    """
    foods = map.getInteractablesByClassifier(Classifiers.FOOD)
    waters = map.getInteractablesByClassifier(Classifiers.WATER)
    rests = map.getInteractablesByClassifier(Classifiers.REST)

    walkingAffinity = player.affinities.walking
    weights = player.affinities.getWeigths()
    # Determine the weight of all entities based on the formula:
    # typeWeight * (walkingAffinity / distance to entity) / affectedStat
    foodsWeights = []
    hunger = player.statistics.hunger
    for food in foods:
        distance = abs(player.x - food.x) + abs(player.y - food.y)
        typeWeight = weights[0]
        foodsWeights.append((typeWeight * (walkingAffinity / distance)) * hunger)

    watersWeights = []
    thirst = player.statistics.thirst
    for water in waters:
        distance = abs(player.x - water.x) + abs(player.y - water.y)
        typeWeight = weights[1]
        watersWeights.append((typeWeight * (walkingAffinity / distance)) * thirst)

    restsWeights = []
    stamina = player.statistics.stamina
    for rest in rests:
        distance = abs(player.x - rest.x) + abs(player.y - rest.y)
        typeWeight = weights[2]
        restsWeights.append((typeWeight * (walkingAffinity / distance)) / stamina)

    finalEntities = foods + waters + rests
    finalWeights = foodsWeights + watersWeights + restsWeights

    if not finalEntities:
        # If all items are gone, pick random one
        finalEntities = map.getInteractablesByClassifier()
    rng = random.Random()
    choice = rng.choices(finalEntities, finalWeights)[0]
    return choice
