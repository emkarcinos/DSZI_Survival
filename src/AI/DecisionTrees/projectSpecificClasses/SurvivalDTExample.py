from src.AI.DecisionTrees.Attribute import Attribute
from src.AI.DecisionTrees.DecisionTreeExample import DecisionTreeExample
from src.AI.DecisionTrees.projectSpecificClasses.DistFromObject import DistFromObject
from src.AI.DecisionTrees.projectSpecificClasses.PlayerStatsValue import PlayerStatsValue
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalAttributesDefinitions import SurvivalAttributesDefinitions
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalClassification import SurvivalClassification


class SurvivalDTExample(DecisionTreeExample):
    """
    This class will be used to create examples for decision trees with project specific attributes like hunger,
    distance from food, etc.
    """
    hungerVal: PlayerStatsValue
    thirstVal: PlayerStatsValue
    staminaVal: PlayerStatsValue
    distFromFood: DistFromObject
    distFromWater: DistFromObject
    distFromRestPlace: DistFromObject

    def __init__(self, classification: SurvivalClassification, hungerVal: PlayerStatsValue, thirstVal: PlayerStatsValue,
                 staminaVal: PlayerStatsValue, distFromFood: DistFromObject, distFromWater: DistFromObject,
                 distFromRestPlace: DistFromObject):
        self.hungerVal = hungerVal
        self.thirstVal = thirstVal
        self.staminaVal = staminaVal
        self.distFromFood = distFromFood
        self.distFromWater = distFromWater
        self.distFromRestPlace = distFromRestPlace

        attributes = [Attribute(SurvivalAttributesDefinitions.hungerAttrDef, hungerVal),
                      Attribute(SurvivalAttributesDefinitions.thirstAttrDef, thirstVal),
                      Attribute(SurvivalAttributesDefinitions.staminaAttrDef, staminaVal),
                      Attribute(SurvivalAttributesDefinitions.foodDistanceAttrDef, distFromFood),
                      Attribute(SurvivalAttributesDefinitions.waterDistanceAttrDef, distFromWater),
                      Attribute(SurvivalAttributesDefinitions.restDistanceAttrDef, distFromRestPlace)]

        super().__init__(classification, attributes)