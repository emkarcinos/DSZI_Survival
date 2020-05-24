from typing import List

from src.AI.DecisionTrees.DecisionTree import DecisionTree
from src.AI.DecisionTrees.projectSpecificClasses.DTEntities.DTSurvivalInteractable import DTSurvivalInteractable
from src.AI.DecisionTrees.projectSpecificClasses.DTPlayerStats import DTPlayerStats
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalClassification import SurvivalClassification
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalDTExample import SurvivalDTExample
from src.AI.GA_With_DT import pickEntityAfterTreeDecision
from src.entities.Enums import Classifiers


class SurvivalDT:
    """
    This class will be used to pick movement target for the player.
    """

    def __init__(self, entityPickingDecisionTree: DecisionTree):
        self.entityPickingDecisionTree = entityPickingDecisionTree

    def pickEntity(self, player, map):
        """
        Select an entity to become the next goal for the player.

        :param player: Player object
        :param map: Map object
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

        treeDecision, choice = pickEntityAfterTreeDecision(currentSituation, self.entityPickingDecisionTree, dtFoods,
                                                           dtRestPlaces, dtWaters)

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

            treeDecision, choice = pickEntityAfterTreeDecision(currentSituation, self.entityPickingDecisionTree, dtFoods,
                                                               dtRestPlaces, dtWaters)

        return choice