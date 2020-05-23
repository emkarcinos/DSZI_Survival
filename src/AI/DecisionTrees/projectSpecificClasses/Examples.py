from src.AI.DecisionTrees.projectSpecificClasses.SurvivalClassification import SurvivalClassification
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalDTExample import SurvivalDTExample
from src.AI.DecisionTrees.projectSpecificClasses.PlayerStatsValue import PlayerStatsValue as Stats
from src.AI.DecisionTrees.projectSpecificClasses.DistFromObject import DistFromObject as Dist

examples = [
    SurvivalDTExample(SurvivalClassification.WATER,
                      Stats.HALF_TO_THREE_QUARTERS,
                      Stats.QUARTER_TO_HALF,
                      Stats.QUARTER_TO_HALF,
                      Dist.GE_3_LT_8,
                      Dist.GE_8,
                      Dist.LT_3),

    SurvivalDTExample(SurvivalClassification.FOOD,
                      Stats.HALF_TO_THREE_QUARTERS,
                      Stats.QUARTER_TO_HALF,
                      Stats.QUARTER_TO_HALF,
                      Dist.LT_3,
                      Dist.GE_8,
                      Dist.GE_8),

]