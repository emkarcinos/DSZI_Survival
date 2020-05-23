from src.AI.DecisionTrees.projectSpecificClasses.DistFromObject import DistFromObject
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalClassification import SurvivalClassification


class DTSurvivalEntity:
    DistFromObjectFromPlayer: DistFromObject

    def __init__(self, distanceFromPlayer: DistFromObject, classification: SurvivalClassification):
        self.classification = classification
        self.distanceFromPlayer = distanceFromPlayer
