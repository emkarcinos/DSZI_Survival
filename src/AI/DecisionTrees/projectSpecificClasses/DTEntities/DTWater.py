from src.AI.DecisionTrees.projectSpecificClasses.DTEntities.DTSurvivalEntity import DTSurvivalEntity
from src.AI.DecisionTrees.projectSpecificClasses.DistFromObject import DistFromObject
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalClassification import SurvivalClassification


class DTWater(DTSurvivalEntity):
    def __init__(self, distanceFromPlayer: DistFromObject):
        super().__init__(distanceFromPlayer)
        self.classification = SurvivalClassification.WATER
