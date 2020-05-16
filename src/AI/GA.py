import random
import numpy

from src.AI.Affinities import Affinities
from src.entities.Enums import Classifiers
from src.entities.Player import Player


def geneticAlgorithm(map, iter, solutions):
    """
    This algorithm will attempt to find the best affinities for player's goal choices.

    :param map: Map with all entities
    :param iter: Generations count
    :param solutions: Solutions per generation
    """
    # Based on 4 weights, that are affinities tied to the player
    weightsCount = 4
    populationSize = (solutions, weightsCount)

    # Initialize the first population with random values
    initialPopulation = numpy.random.uniform(low=0.0, high=1.0, size=populationSize)
    population = initialPopulation
    for i in range(iter):
        fitness = []
        for player in population:
            fitness.append(doSimulation(player, map))


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
    print(fitness)
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

    return random.choices(finalEntities, finalWeights)[0]
