from src.AI.DecisionTrees.AttributeDefinition import AttributeDefinition
from src.AI.DecisionTrees.projectSpecificClasses.DistFromObject import DistFromObject
from src.AI.DecisionTrees.projectSpecificClasses.PlayerStatsValue import PlayerStatsValue


class SurvivalAttributesDefinitions:
    """
    This class contains all attributes definitions which will be used to create decision tree examples
    and decision tree learning.

    There are definitions of attributes like hunger, thirst, etc...
    """

    attrsDefinitionsCount = 6

    hungerAttrDef = AttributeDefinition(0, "Hunger", [PlayerStatsValue.ZERO_TO_QUARTER,
                                                      PlayerStatsValue.QUARTER_TO_HALF,
                                                      PlayerStatsValue.HALF_TO_THREE_QUARTERS,
                                                      PlayerStatsValue.THREE_QUARTERS_TO_FULL])

    thirstAttrDef = AttributeDefinition(1, "Thirst", [PlayerStatsValue.ZERO_TO_QUARTER,
                                                      PlayerStatsValue.QUARTER_TO_HALF,
                                                      PlayerStatsValue.HALF_TO_THREE_QUARTERS,
                                                      PlayerStatsValue.THREE_QUARTERS_TO_FULL])

    staminaAttrDef = AttributeDefinition(2, "Stamina", [PlayerStatsValue.ZERO_TO_QUARTER,
                                                        PlayerStatsValue.QUARTER_TO_HALF,
                                                        PlayerStatsValue.HALF_TO_THREE_QUARTERS,
                                                        PlayerStatsValue.THREE_QUARTERS_TO_FULL])

    foodDistanceAttrDef = AttributeDefinition(3, "Distance from food",
                                              [DistFromObject.LT_3, DistFromObject.GE_3_LT_8, DistFromObject.GE_8])

    waterDistanceAttrDef = AttributeDefinition(4, "Distance from water",
                                              [DistFromObject.LT_3, DistFromObject.GE_3_LT_8, DistFromObject.GE_8])

    restDistanceAttrDef = AttributeDefinition(5, "Distance from rest place",
                                              [DistFromObject.LT_3, DistFromObject.GE_3_LT_8, DistFromObject.GE_8])

    allAttributesDefinitions = [hungerAttrDef, thirstAttrDef, staminaAttrDef,
                                foodDistanceAttrDef, waterDistanceAttrDef, restDistanceAttrDef]
