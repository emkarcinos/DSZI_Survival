import random
from datetime import datetime
from typing import List

import numpy

import src.AI.DecisionTrees.InductiveDecisionTreeLearning as DT
import src.AI.DecisionTrees.projectSpecificClasses.Examples as Examples
from src.AI.Affinities import Affinities
from src.AI.DecisionTrees.DecisionTree import DecisionTree
from src.AI.DecisionTrees.projectSpecificClasses.DTEntities.DTSurvivalInteractable import DTSurvivalInteractable
from src.AI.DecisionTrees.projectSpecificClasses.DTPlayerStats import DTPlayerStats
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalAttributesDefinitions import \
    SurvivalAttributesDefinitions as AttrDefs
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalClassification import SurvivalClassification
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalDTExample import SurvivalDTExample
from src.entities.Enums import Classifiers
from src.entities.Player import Player
from src.game.Map import Map


def geneticAlgorithmWithDecisionTree(map, iter, solutions, mutationAmount=0.05):
    """
    This is fusion of genetic algorithm and decision tree. Decision tree is giving travel goals for player.

    :param map: Map with all entities
    :param iter: Generations count
    :param solutions: Solutions per generation
    :param mutationAmount: Mutation strength
    """

    entityPickingDecisionTree = DT.inductiveDecisionTreeLearning(Examples.examples,
                                                                 AttrDefs.allAttributesDefinitions,
                                                                 SurvivalClassification.FOOD,
                                                                 SurvivalClassification)

    print("\nDecision tree: \n")
    DecisionTree.printTree(entityPickingDecisionTree, 0)
    print()

    # Based on 4 weights, that are affinities tied to the player
    weightsCount = 4

    # Initialize the first population with random values
    initialPopulation = numpy.random.uniform(low=0.0, high=1.0, size=(solutions, weightsCount))
    population = initialPopulation
    maps = []

    # Set the RNG seed for this GA
    # 125 is good for weak start
    random.seed(125)
    # Begin
    for i in range(iter):
        print("\nRunning {} generation...".format(i + 1))

        # random.seed(random.randrange(0, 100000))
        fitness = []

        for player in population:
            fitness.append(doSimulation(player, map, entityPickingDecisionTree))

        parents = selectMatingPool(population, fitness, int(solutions / 2))

        print("Best fitness: {}".format(max(fitness)))
        offspring = mating(parents, solutions, mutationAmount)
        print("Best offspring: ", offspring[0])

        writeResults(i, max(fitness), offspring[0])

        population = offspring


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
    """
    Apply a random offset to a random gene.

    :param offspring: Array of offspring
    :param mutationAmount: How strong the mutation is
    :return: Offspring after mutation
    """
    for player in offspring:
        randomGeneIdx = random.randrange(0, len(player))
        player[randomGeneIdx] = player[randomGeneIdx] + random.uniform(-1.0, 1.0) * mutationAmount
    return offspring


def doSimulation(weights, map, decisionTree):
    """
    Runs the simulation. Returns fitness.

    :param weights: A list of weights for players.
    :param map: Map object
    """
    player = Player((6, 2), map.tileSize, Affinities(weights[0], weights[1], weights[2], weights[3]))
    player.disableMovementTime()
    while player.alive:
        if player.movementTarget is None:
            target = pickEntity(player, map, decisionTree)
            player.gotoToTarget(target, map)
        player.update()
    fitness = player.movePoints
    player.kill()
    del player
    map.respawn()
    return fitness


def pickEntity(player, map, entityPickingDecisionTree: DecisionTree):
    """
    Select an entity to become the next goal for the player. The goal is specified by decision tree.

    :param entityPickingDecisionTree: 
    :param player: Player object
    :param map: Map object
    :type map: Map
    :type player: Player
    """
    foods = map.getInteractablesByClassifier(Classifiers.FOOD)
    waters = map.getInteractablesByClassifier(Classifiers.WATER)
    rests = map.getInteractablesByClassifier(Classifiers.REST)

    playerStats = DTPlayerStats.dtStatsFromPlayerStats(player.statistics)

    # Get foods sorted by distance from player
    dtFoods: List[DTSurvivalInteractable] = []
    for food in foods:
        dtFood = DTSurvivalInteractable.dtInteractableFromInteractable(food, player.x, player.y)
        dtFoods.append(dtFood)

    dtFoods.sort(key=lambda x: x.distanceFromPlayer.value)

    # Get waters sorted by distance from player
    dtWaters: List[DTSurvivalInteractable] = []
    for water in waters:
        dtWater = DTSurvivalInteractable.dtInteractableFromInteractable(water, player.x, player.y)
        dtWaters.append(dtWater)
    dtWaters.sort(key=lambda x: x.distanceFromPlayer.value)

    # Get rest places sorted by distance from player
    dtRestPlaces: List[DTSurvivalInteractable] = []
    for rest in rests:
        dtRest = DTSurvivalInteractable.dtInteractableFromInteractable(rest, player.x, player.y)
        dtRestPlaces.append(dtRest)
    dtRestPlaces.sort(key=lambda x: x.distanceFromPlayer.value)

    currentSituation = SurvivalDTExample(None, playerStats.hungerAmount, playerStats.thirstAmount,
                                         playerStats.staminaAmount,
                                         dtFoods[0].distanceFromPlayer, dtWaters[0].distanceFromPlayer,
                                         dtRestPlaces[0].distanceFromPlayer)

    treeDecision, choice = pickEntityAfterTreeDecision(currentSituation, entityPickingDecisionTree, dtFoods, dtRestPlaces, dtWaters)

    # If the choice happens to be the same as the last one pick something else.
    if choice == map.getEntityOnCoord(player.getFacingCoord()):
        if treeDecision == SurvivalClassification.FOOD:
            dtFoods.remove(dtFoods[0])
        elif treeDecision == SurvivalClassification.WATER:
            dtWaters.remove(dtWaters[0])
        elif treeDecision == SurvivalClassification.REST:
            dtRestPlaces.remove(dtRestPlaces[0])

        currentSituation = SurvivalDTExample(None, playerStats.hungerAmount, playerStats.thirstAmount,
                                             playerStats.staminaAmount,
                                             dtFoods[0].distanceFromPlayer, dtWaters[0].distanceFromPlayer,
                                             dtRestPlaces[0].distanceFromPlayer)

        treeDecision, choice = pickEntityAfterTreeDecision(currentSituation, entityPickingDecisionTree, dtFoods, dtRestPlaces, dtWaters)

    return choice


def pickEntityAfterTreeDecision(currentSituation, decisionTree, dtFoods, dtRestPlaces, dtWaters):

    treeDecision = decisionTree.giveAnswer(currentSituation)
    choice = None
    if treeDecision == SurvivalClassification.FOOD:
        choice = dtFoods[0].interactable
    elif treeDecision == SurvivalClassification.WATER:
        choice = dtWaters[0].interactable
    elif treeDecision == SurvivalClassification.REST:
        choice = dtRestPlaces[0].interactable
    return treeDecision, choice


def writeResults(iter, bestFit, bestMember):
    """
    Logs the results of the iteration to files.
    The function will create two files - one that is human-readable,
    and the other as Raw data used for plotting and analysis.
    The output file is fixed to src/AI/resultsExplorer/.

    :param iter: Current iteration index
    :param bestFit: Best fitness in this generation
    :param bestMember: Array of affinities of the best member in the generation
    """
    if iter == 0:
        # Initialize human-readable log file
        with open("src/AI/resultsExplorer/results.txt", "w+") as f:
            f.write("GA Results from " + str(datetime.now()))
            f.write("\n")

        with open("src/AI/resultsExplorer/resultsRaw.txt", "w+") as f:
            f.write("=HEADER=GA=\n")

    with open("src/AI/resultsExplorer/results.txt", "a") as f:
        f.write("Population: {}\n".format(iter))
        f.write("Best fitness: {}\n".format(bestFit))
        f.write("Best offspring: " + str(bestMember))
        f.write("\n\n")

    # Write raw arrays
    with open("src/AI/resultsExplorer/resultsRaw.txt", "a") as f:
        f.write(str(bestMember + [bestFit]))
        f.write("\n")
