import math
from typing import List

from src.AI.DecisionTrees.AttributeDefinition import AttributeDefinition
from src.AI.DecisionTrees.DecisionTree import DecisionTree
from src.AI.DecisionTrees.DecisionTreeBranch import DecisionTreeBranch
from src.AI.DecisionTrees.DecisionTreeExample import DecisionTreeExample


def inductiveDecisionTreeLearning(examples: List[DecisionTreeExample], attributes: List[AttributeDefinition], default,
                                  classifications):
    """
    Builds decision tree based on given examples and attributes and possible classifications.

    :param examples:
    :param attributes: List of all attributes definitions.
    :param default: Default classification.
    :param classifications: Possible example classifications.
    :return: Decision Tree.
    """

    # If there are no examples return default.
    if examples is None or len(examples) == 0:
        return DecisionTree(default)

    # If all examples belong to the same classification then return node with that classification.
    elif checkIfAllExamplesHaveSameClassification(examples):
        return DecisionTree(examples[0].classification)

    # If there are no attributes then return node with classification majority.
    elif attributes is None or len(attributes) == 0:
        return majorityValue(examples)

    else:
        best = chooseAttribute(attributes, examples, classifications)
        tree = DecisionTree(best)

        for value in best.values:
            examples_i = getElementsWithAttributeValue(examples, best, value)
            subtree = inductiveDecisionTreeLearning(examples_i, attributes, majorityValue(examples), classifications)
            tree.addBranch(DecisionTreeBranch(tree, value, subtree))

        return tree


def majorityValue(examples: List[DecisionTreeExample]):
    """
    Returns classification which most of examples have.

    :param examples:
    :return: Classification.
    """
    classifications = []

    # Making list of values
    for example in examples:
        if example.classification not in classifications:
            classifications.append(example.classification)

    # Finding majority value's index
    majorityValueInd = 0
    majorityValueCount = 0
    ind = 0
    for classification in classifications:
        count = 0
        for example in examples:
            if example.classification == classification:
                count += 1
        if count > majorityValueCount:
            majorityValueCount = count
            majorityValueInd = ind

        ind += 1

    return classifications[majorityValueInd]


def checkIfAllExamplesHaveSameClassification(examples: List[DecisionTreeExample]):
    return all([example.classification == examples[0].classification for example in examples])


def probOfExBeingClass(classification, allExamplesNum, classExamplesNum):
    """
    Calculates probability of example being classified as given classification.
    Needed to calculate information entropy.

    :param classExamplesNum: Number of examples classified as given classification
    :param allExamplesNum: Number of all examples
    :param classification:
    """
    if allExamplesNum == 0:
        return 0

    return classExamplesNum / allExamplesNum


def chooseAttribute(attributes: List[AttributeDefinition], examples: List[DecisionTreeExample], classifications):
    """
    Chooses best attribute by calculating information gain for each attribute. Returns attribute with maximum gain.

    :param classifications: All possible classifications.
    :param attributes: All attributes.
    :param examples:
    """
    bestAttribute = None
    bestAttributeGain = -1

    for attribute in attributes:
        attrInformationGain = calculateInformationGain(attribute, classifications, examples)
        if attrInformationGain > bestAttributeGain:
            bestAttribute = attribute
            bestAttributeGain = attrInformationGain

    return bestAttribute


def calculateInformationGain(attribute: AttributeDefinition, classifications, examples: List[DecisionTreeExample]):
    """
    Calculates how much information we will gain after checking value of given attribute.
    Needed to choose best attribute.

    :param attribute:
    :param classifications:
    :param examples:
    :return:
    """
    return calculateEntropy(classifications, examples) - calculateRemainder(attribute, examples, classifications)


def calculateRemainder(attribute: AttributeDefinition, examples: List[DecisionTreeExample], classifications):
    """
    Calculates how much information will be needed to classify an example after checking value of given attribute.
    Needed when calculating information gain.

    :param classifications:
    :param attribute:
    :param examples:
    """

    remainder = 0
    examplesNum = len(examples)

    # Attribute divides examples to subsets
    examplesDividedByAttrValues = {}

    for value in attribute.values:
        examplesWithValue = []
        for example in examples:
            if example.getAttributeWithDefinition(attribute).value == value:
                examplesWithValue.append(example)
        examplesDividedByAttrValues[value] = examplesWithValue

    for value, examplesSubset in examplesDividedByAttrValues.items():
        remainder += (len(examplesSubset) / examplesNum) * calculateEntropy(classifications, examplesSubset)

    return remainder


def calculateEntropy(classifications, examples: List[DecisionTreeExample]):
    """
    Calculates information entropy. Needed when calculating information gain.

    :param classifications:
    :param examples:
    :return:
    """
    examplesNum = len(examples)
    examplesNumByClassification = {}
    for classification in classifications:
        count = 0
        for example in examples:
            if example.classification == classification:
                count += 1
        examplesNumByClassification[classification] = count

    entropy = 0
    for classification in classifications:
        p = probOfExBeingClass(classification, examplesNum, examplesNumByClassification[classification])
        if p == 0:
            pass
        else:
            entropy += (-1) * (p * math.log2(p))

    return entropy


def getElementsWithAttributeValue(examples: List[DecisionTreeExample], attributeDefinition: AttributeDefinition, value):
    """
    Returns subset of examples with given attribute value.

    :param examples:
    :param attributeDefinition:
    :param value:
    :return:
    """
    elements = []
    for example in examples:
        if example.getAttributeWithDefinition(attributeDefinition).value == value:
            elements.append(example)

    return elements
