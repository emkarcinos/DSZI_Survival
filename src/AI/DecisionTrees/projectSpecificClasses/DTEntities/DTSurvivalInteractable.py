from src.AI.DecisionTrees.projectSpecificClasses.DistFromObject import DistFromObject
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalClassification import SurvivalClassification
from src.entities.Enums import Classifiers
from src.entities.Interactable import Interactable


class DTSurvivalInteractable:
    DistFromObjectFromPlayer: DistFromObject

    def __init__(self, dtDistanceFromPlayer: DistFromObject, classification: SurvivalClassification,
                 interactable: Interactable, accurateDistanceFromPlayer: int):
        self.interactable = interactable
        self.classification = classification
        self.dtDistanceFromPlayer = dtDistanceFromPlayer
        self.accurateDistanceFromPlayer = accurateDistanceFromPlayer

    @staticmethod
    def dtInteractableFromInteractable(interactable: Interactable, playerX: int, playerY: int):
        classification = None
        distanceFromPlayer = None

        if interactable.classifier == Classifiers.FOOD:
            classification = SurvivalClassification.FOOD
        elif interactable.classifier == Classifiers.WATER:
            classification = SurvivalClassification.WATER
        elif interactable.classifier == Classifiers.REST:
            classification = SurvivalClassification.REST
        else:
            return None

        distance = abs(playerX - interactable.x) + abs(playerY - interactable.y)

        """
        Add + 1 everywhere, because player doesn't have to step on interactable in order to interact with it.
        So for example if dst between player and object is 3, player has to go 2 fields in order to interact with this object.
        """
        if distance < 3 + 1:
            distanceFromPlayer = DistFromObject.LT_3
        elif 3 + 1 <= distance < 8 + 1:
            distanceFromPlayer = DistFromObject.GE_3_LT_8
        elif 8 + 1 <= distance < 15 + 1:
            distanceFromPlayer = DistFromObject.GE_8_LT_15
        elif distance >= 15 + 1:
            distanceFromPlayer = DistFromObject.GE_15
        else:
            return None

        return DTSurvivalInteractable(distanceFromPlayer, classification, interactable, distance)

    def getDescription(self):
        dsc = "Classification: {}, Distance from player: {}".format(self.classification, self.dtDistanceFromPlayer)
        return dsc

    def getDtDistanceFromOtherInteractable(self, otherInteractable: Interactable):
        """
        Returns distance of this interactable from other interactable as enum, that can be used in decision tree
        learning.

        :param otherInteractable:
        """
        accurateDistance = abs(self.interactable.x - otherInteractable.x) + \
                           abs(self.interactable.y - otherInteractable.y)

        if accurateDistance < 3:
            return DistFromObject.LT_3
        elif 3 <= accurateDistance < 8:
            return DistFromObject.GE_3_LT_8
        elif 8 <= accurateDistance < 15:
            return DistFromObject.GE_8_LT_15
        elif accurateDistance > 15:
            return DistFromObject.GE_15