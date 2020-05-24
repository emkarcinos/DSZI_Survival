import random
from typing import Any, Union, List

from src.AI.DecisionTrees.projectSpecificClasses.DistFromObject import DistFromObject
from src.AI.DecisionTrees.projectSpecificClasses.PlayerStatsValue import PlayerStatsValue
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalAttributesDefinitions import SurvivalAttributesDefinitions
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
            line: str = file.readline()
            if line == "":
                break
            lineNum += 1

            line = line.rstrip('\n')
            words = line.split("|")

            if len(words) != SurvivalAttributesDefinitions.attrsDefinitionsCount + 1:
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

            # Distance from water after food
            parseSuccess = False
            dstFromWaterAfterFood: DistFromObject
            for dstFromWaterAfterFood in DistFromObject:
                if dstFromWaterAfterFood.name == words[7]:
                    parseSuccess = True
                    break
            if not parseSuccess:
                print("Distance from water after food not parsed at line {}.".format(str(lineNum)))
                continue

            example = SurvivalDTExample(classification,
                                        hungerAmount,
                                        thirstAmount,
                                        staminaAmount,
                                        dstFromFood,
                                        dstFromWater,
                                        dstFromRest,
                                        dstFromWaterAfterFood)

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
            strToWrite = "{}|{}|{}|{}|{}|{}|{}|{}\n".format(example.classification.name,
                                                            example.hungerVal.name,
                                                            example.thirstVal.name,
                                                            example.staminaVal.name,
                                                            example.distFromFood.name,
                                                            example.distFromWater.name,
                                                            example.distFromRestPlace.name,
                                                            example.dstFromWaterAfterFood.name)
            file.write(strToWrite)
        file.close()

    def generateExamples(self):
        # retrieve list of examples that are currently saved in file - they will be needed to check for duplicates
        examplesThatAreInFile = self.readExamples()

        # make list of all possible values
        statsValues = [value for value in PlayerStatsValue]
        distances = [value for value in DistFromObject]

        while True:

            howManyExamplesGenerate = int(input("How many example do you want to generate? : "))
            print()

            for i in range(howManyExamplesGenerate):

                print("Generating example {} ...".format(str(i + 1)))

                # pick random values from each list and make survival example out of them, with None classification
                newExample = SurvivalDTExample(None,
                                               random.choice(statsValues),
                                               random.choice(statsValues),
                                               random.choice(statsValues),
                                               random.choice(distances),
                                               random.choice(distances),
                                               random.choice(distances),
                                               random.choice(distances))

                # check if made example is not a duplicate
                isDuplicate = False

                possibleDuplicate: SurvivalDTExample
                for possibleDuplicate in examplesThatAreInFile:
                    if possibleDuplicate.compareAttributes(newExample):
                        isDuplicate = True
                        break

                if isDuplicate:
                    # return to create new example
                    print("Generated duplicate.")
                    i -= 1
                    continue

                # if not a duplicate then ask for classification
                print()
                print("Generated example: \n{}".format(newExample.getDescription()))
                print()

                givenClsIsGood = False
                while not givenClsIsGood:
                    strClassification = input("What is classification of this example? : ")
                    for classification in SurvivalClassification:
                        if classification.name == strClassification:
                            givenClsIsGood = True
                            break
                    if not givenClsIsGood:
                        print("There is no such classification. Possible classifications: {}".
                              format(str([cls.name for cls in SurvivalClassification])))

                # set example's classification and append it to examples file.
                newExample.classification = classification
                self.addExamplesToFile([newExample])

            keepGenerating = input("Type 'E' to stop generating or anything else to continue.\n")
            if keepGenerating == "E":
                break
