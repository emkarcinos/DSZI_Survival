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

    def compareAttributes(self, anotherExample) -> bool:
        """
        Compares attributes of this example with another example's attributes.

        :param anotherExample:
        :return: True if attrs are equal, False otherwise
        """
        attrsAreEqual = True

        if self.hungerVal != anotherExample.hungerVal:
            attrsAreEqual = False
        elif self.thirstVal != anotherExample.thirstVal:
            attrsAreEqual = False
        elif self.staminaVal != anotherExample.staminaVal:
            attrsAreEqual = False
        elif self.distFromFood != anotherExample.distFromFood:
            attrsAreEqual = False
        elif self.distFromWater != anotherExample.distFromWater:
            attrsAreEqual = False
        elif self.distFromRestPlace != anotherExample.distFromRestPlace:
            attrsAreEqual = False

        return attrsAreEqual

    def getDescription(self):
        dsc = "Classification: {}".format(self.classification)
        dsc += "\nHunger: {}".format(self.hungerVal.name)
        dsc += "\nThirst: {}".format(self.thirstVal.name)
        dsc += "\nStamina: {}".format(self.staminaVal.name)
        dsc += "\nDistance from food: {}".format(self.distFromFood.name)
        dsc += "\nDistance from water: {}".format(self.distFromWater.name)
        dsc += "\nDistance from rest place: {}".format(self.distFromRestPlace.name)

        return dsc
