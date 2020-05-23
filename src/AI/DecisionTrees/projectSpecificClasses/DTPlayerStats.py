from src.AI.DecisionTrees.projectSpecificClasses.PlayerStatsValue import PlayerStatsValue
from src.entities.Statistics import Statistics


class DTPlayerStats:
    hungerAmount: PlayerStatsValue
    thirstAmount: PlayerStatsValue
    staminaAmount: PlayerStatsValue

    def __init__(self, hungerAmount: PlayerStatsValue, thirstAmount: PlayerStatsValue, staminaAmount: PlayerStatsValue):
        self.staminaAmount = staminaAmount
        self.thirstAmount = thirstAmount
        self.hungerAmount = hungerAmount

    @staticmethod
    def dtStatsFromPlayerStats(playerStatistics: Statistics):
        """
        This method converts player statistics to object representing statistics that can be used in decision tree.

        :param playerStatistics:
        """

        hunger = playerStatistics.hunger / 100  # 100 is max value
        thirst = playerStatistics.thirst / 100
        stamina = playerStatistics.stamina / 100

        hungerAmount = None
        if hunger <= 0.25:
            hungerAmount = PlayerStatsValue.ZERO_TO_QUARTER
        elif 0.25 < hunger < 0.5:
            hungerAmount = PlayerStatsValue.QUARTER_TO_HALF
        elif 0.5 <= hunger < 0.75:
            hungerAmount = PlayerStatsValue.HALF_TO_THREE_QUARTERS
        else:   # 0.75 <= hunger <= 1
            hungerAmount = PlayerStatsValue.THREE_QUARTERS_TO_FULL
            
        thirstAmount = None
        if thirst <= 0.25:
            thirstAmount = PlayerStatsValue.ZERO_TO_QUARTER
        elif 0.25 < thirst < 0.5:
            thirstAmount = PlayerStatsValue.QUARTER_TO_HALF
        elif 0.5 <= thirst < 0.75:
            thirstAmount = PlayerStatsValue.HALF_TO_THREE_QUARTERS
        else:   # 0.75 <= thirst <= 1
            thirstAmount = PlayerStatsValue.THREE_QUARTERS_TO_FULL
            
        staminaAmount = None
        if stamina <= 0.25:
            staminaAmount = PlayerStatsValue.ZERO_TO_QUARTER
        elif 0.25 < stamina < 0.5:
            staminaAmount = PlayerStatsValue.QUARTER_TO_HALF
        elif 0.5 <= stamina < 0.75:
            staminaAmount = PlayerStatsValue.HALF_TO_THREE_QUARTERS
        else:   # 0.75 <= stamina <= 1
            staminaAmount = PlayerStatsValue.THREE_QUARTERS_TO_FULL

        return DTPlayerStats(hungerAmount, thirstAmount, staminaAmount)
