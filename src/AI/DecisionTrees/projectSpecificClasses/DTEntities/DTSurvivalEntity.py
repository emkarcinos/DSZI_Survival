from src.AI.DecisionTrees.projectSpecificClasses.DistFromObject import DistFromObject


class DTSurvivalEntity:
    DistFromObjectFromPlayer: DistFromObject

    def __init__(self, distanceFromPlayer: DistFromObject):
        self.distanceFromPlayer = distanceFromPlayer
