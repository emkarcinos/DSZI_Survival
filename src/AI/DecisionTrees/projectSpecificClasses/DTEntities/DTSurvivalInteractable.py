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

        if distance < 3:
            distanceFromPlayer = DistFromObject.LT_3
        elif 3 <= distance < 8:
            distanceFromPlayer = DistFromObject.GE_3_LT_8
        elif 8 <= distance < 15:
            distanceFromPlayer = DistFromObject.GE_8_LT_15
        elif distance >= 15:
            distanceFromPlayer = DistFromObject.GE_15
        else:
            return None

        return DTSurvivalInteractable(distanceFromPlayer, classification, interactable, distance)

    def getDescription(self):
        dsc = "Classification: {}, Distance from player: {}".format(self.classification, self.dtDistanceFromPlayer)
        return dsc
