from typing import Any, Union, List

from src.AI.DecisionTrees.projectSpecificClasses.DistFromObject import DistFromObject
from src.AI.DecisionTrees.projectSpecificClasses.PlayerStatsValue import PlayerStatsValue
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalClassification import SurvivalClassification
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalDTExample import SurvivalDTExample


class ExamplesManager:

    def __init__(self, examplesFilePath: str):
        self.examplesFilePath = examplesFilePath

    def readExamples(self):
        """
        This method reads examples for decision tree learning from file.

        :return: List of read examples.
        """
        examples = []

        file = open(self.examplesFilePath, "r")

        lineNum = 0
        while True:
            line = file.readline()
            if line == "":
                break
            lineNum += 1
            words = line.split("|")

            if len(words) != 7:
                print("Not sufficient amount of words in line {}.".format(str(lineNum)))
                continue

            # Classification
            parseSuccess = False
            classification: SurvivalClassification
            for classification in SurvivalClassification:
                if words[0] == classification.name:
                    parseSuccess = True
                    break
            if not parseSuccess:
                print("Example classification not parsed at line {}.".format(str(lineNum)))
                continue

            # Hunger value
            parseSuccess = False
            hungerAmount: PlayerStatsValue
            for hungerAmount in PlayerStatsValue:
                if hungerAmount.name == words[1]:
                    parseSuccess = True
                    break
            if not parseSuccess:
                print("Hunger not parsed at line {}.".format(str(lineNum)))
                continue

            # Thirst value
            parseSuccess = False
            thirstAmount: PlayerStatsValue
            for thirstAmount in PlayerStatsValue:
                if thirstAmount.name == words[2]:
                    parseSuccess = True
                    break
            if not parseSuccess:
                print("Thirst not parsed at line {}.".format(str(lineNum)))
                continue

            # Stamina value
            parseSuccess = False
            staminaAmount: PlayerStatsValue
            for staminaAmount in PlayerStatsValue:
                if staminaAmount.name == words[3]:
                    parseSuccess = True
                    break
            if not parseSuccess:
                print("Stamina not parsed at line {}.".format(str(lineNum)))
                continue

            # Distance from food
            parseSuccess = False
            dstFromFood: DistFromObject
            for dstFromFood in DistFromObject:
                if dstFromFood.name == words[4]:
                    parseSuccess = True
                    break
            if not parseSuccess:
                print("Distance from food not parsed at line {}.".format(str(lineNum)))
                continue

            # Distance from water
            parseSuccess = False
            dstFromWater: DistFromObject
            for dstFromWater in DistFromObject:
                if dstFromWater.name == words[5]:
                    parseSuccess = True
                    break
            if not parseSuccess:
                print("Distance from water not parsed at line {}.".format(str(lineNum)))
                continue

            # Distance from rest place
            parseSuccess = False
            dstFromRest: DistFromObject
            for dstFromRest in DistFromObject:
                if dstFromRest.name == words[6]:
                    parseSuccess = True
                    break
            if not parseSuccess:
                print("Distance from rest place not parsed at line {}.".format(str(lineNum)))
                continue

            example = SurvivalDTExample(classification,
                                        hungerAmount,
                                        thirstAmount,
                                        staminaAmount,
                                        dstFromFood,
                                        dstFromWater,
                                        dstFromRest)

            examples.append(example)
        file.close()

        return examples

    def addExamplesToFile(self, examplesToAdd: List[SurvivalDTExample]):
        """
        Appends given examples to examples file.

        :param examplesToAdd:
        """
        file = open(self.examplesFilePath, "a+")

        example: SurvivalDTExample
        for example in examplesToAdd:
            strToWrite = "\n{}|{}|{}|{}|{}|{}|{}".format(example.classification.name,
                                                         example.hungerVal.name,
                                                         example.thirstVal.name,
                                                         example.staminaVal.name,
                                                         example.distFromFood.name,
                                                         example.distFromWater.name,
                                                         example.distFromRestPlace.name)
            file.write(strToWrite)
        file.close()
