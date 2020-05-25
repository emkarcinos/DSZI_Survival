import random

from typing import List

from src.AI.DecisionTrees.DecisionTreeExample import DecisionTreeExample
from src.AI.DecisionTrees.InductiveDecisionTreeLearning import inductiveDecisionTreeLearning
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalAttributesDefinitions import SurvivalAttributesDefinitions
from src.AI.DecisionTrees.projectSpecificClasses.SurvivalClassification import SurvivalClassification


def testDecisionTree(examples: List[DecisionTreeExample], iterations=10, partOfExamplesAsTrainingSet=0.9):
    examplesNum = len(examples)
    trainingSetSize = int(examplesNum * partOfExamplesAsTrainingSet)
    testSetSize = examplesNum - trainingSetSize

    treeScores = []

    for i in range(iterations):
        # Shuffling examples
        random.shuffle(examples)
        # Test and training set
        trainingSet = examples[:trainingSetSize]
        testSet = examples[trainingSetSize:]

        # Create decision tree out of training set
        dt = inductiveDecisionTreeLearning(trainingSet, SurvivalAttributesDefinitions.allAttributesDefinitions,
                                           SurvivalClassification.FOOD, SurvivalClassification)

        # Check how many answers will be correct for test set
        correctAnswers = 0
        for testExample in testSet:
            dtAnswer = dt.giveAnswer(testExample)
            if dtAnswer == testExample.classification:
                correctAnswers += 1

        treeScores.append(correctAnswers / testSetSize)

    return treeScores

