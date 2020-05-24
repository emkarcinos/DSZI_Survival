from typing import List

from src.AI.DecisionTrees.DecisionTree import DecisionTree
from src.AI.DecisionTrees.projectSpecificClasses.DTEntities.DTSurvivalInteractable import DTSurvivalInteractable
from src.AI.DecisionTrees.projectSpecificClasses.DTPlayerStats import DTPlayerStats
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalClassification import SurvivalClassification
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalDTExample import SurvivalDTExample
from src.entities.Enums import Classifiers


class SurvivalDT:
    """
    This class will be used to pick movement target for the player.
    """

    def __init__(self, entityPickingDecisionTree: DecisionTree):
        self.entityPickingDecisionTree = entityPickingDecisionTree

    def pickEntity(self, player, map, pickForGa=False):
        """
        Select an entity to become the next goal for the player.

        :param pickForGa: If picking is done for genetic algorithm then pick can't be the same as last.
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

        dtFoods.sort(key=lambda x: x.accurateDistanceFromPlayer)
        nearestDtFood = dtFoods[0]

        # Get waters sorted by distance from player
        dtWaters: List[DTSurvivalInteractable] = []
        for water in waters:
            dtWater = DTSurvivalInteractable.dtInteractableFromInteractable(water, player.x, player.y)
            dtWaters.append(dtWater)
        dtWaters.sort(key=lambda x: x.accurateDistanceFromPlayer)
        nearestDtWater = dtWaters[0]

        # Get rest places sorted by distance from player
        dtRestPlaces: List[DTSurvivalInteractable] = []
        for rest in rests:
            dtRest = DTSurvivalInteractable.dtInteractableFromInteractable(rest, player.x, player.y)
            dtRestPlaces.append(dtRest)
        dtRestPlaces.sort(key=lambda x: x.accurateDistanceFromPlayer)
        nearestDtRest = dtRestPlaces[0]

        currentSituation = SurvivalDTExample(None, playerStats.hungerAmount, playerStats.thirstAmount,
                                             playerStats.staminaAmount,
                                             nearestDtFood.dtDistanceFromPlayer, nearestDtWater.dtDistanceFromPlayer,
                                             nearestDtRest.dtDistanceFromPlayer,
                                             nearestDtFood.getDtDistanceFromOtherInteractable(nearestDtWater.interactable))

        treeDecision, choice = self.__pickEntityAfterTreeDecision__(currentSituation,
                                                                    dtFoods,
                                                                    dtRestPlaces,
                                                                    dtWaters)

        """
        If choice is being made for genetic algorithm then do not allow to pick same entity as before,
        because fitness is being calculated by travelled fields, not time being alive.
        So player shouldn't be standing and drinking water, but moving from one water field to another.
        """
        if pickForGa:
            # If the choice happens to be the same as the last one pick something else.
            if choice.interactable == map.getEntityOnCoord(player.getFacingCoord()):
                if treeDecision == SurvivalClassification.FOOD:
                    dtFoods.remove(dtFoods[0])
                    nearestDtFood = dtFoods[0]
                elif treeDecision == SurvivalClassification.WATER:
                    dtWaters.remove(dtWaters[0])
                    nearestDtWater = dtWaters[0]
                elif treeDecision == SurvivalClassification.REST:
                    dtRestPlaces.remove(dtRestPlaces[0])
                    nearestDtRest = dtRestPlaces[0]

                currentSituation = SurvivalDTExample(None, playerStats.hungerAmount, playerStats.thirstAmount,
                                                     playerStats.staminaAmount,
                                                     nearestDtFood.dtDistanceFromPlayer, nearestDtWater.dtDistanceFromPlayer,
                                                     nearestDtRest.dtDistanceFromPlayer,
                                                     nearestDtFood.getDtDistanceFromOtherInteractable(nearestDtWater.interactable))

                treeDecision, choice = self.__pickEntityAfterTreeDecision__(currentSituation, dtFoods,
                                                                            dtRestPlaces, dtWaters)

        return choice.interactable

    def __pickEntityAfterTreeDecision__(self, currentSituation, dtFoods, dtRestPlaces, dtWaters):
        """
        This method is usable only in SurvivalDT.pickEntity method.

        After decision tree decides for what type of entity player should go this method retrieves a proper object
        from list of foods, rest places, waters.

        :param currentSituation:
        :param dtFoods:
        :param dtRestPlaces:
        :param dtWaters:
        :return:
        """
        treeDecision = self.entityPickingDecisionTree.giveAnswer(currentSituation)
        choice = None
        if treeDecision == SurvivalClassification.FOOD:
            choice = dtFoods[0]
        elif treeDecision == SurvivalClassification.WATER:
            choice = dtWaters[0]
        elif treeDecision == SurvivalClassification.REST:
            choice = dtRestPlaces[0]
        return treeDecision, choice
