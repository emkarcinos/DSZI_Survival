from src.AI.DecisionTrees.projectSpecificClasses.PlayerStatsValue import PlayerStatsValue


class DTPlayerStats:
    hungerAmount: PlayerStatsValue
    thirstAmount: PlayerStatsValue
    staminaAmount: PlayerStatsValue

    def __init__(self, hungerAmount: PlayerStatsValue, thirstAmount: PlayerStatsValue, staminaAmount: PlayerStatsValue):
        self.staminaAmount = staminaAmount
        self.thirstAmount = thirstAmount
        self.hungerAmount = hungerAmount
