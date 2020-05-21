from typing import List

from src.AI.DecisionTrees.Attribute import Attribute
from src.AI.DecisionTrees.AttributeDefinition import AttributeDefinition


class DecisionTreeExample:
    def __init__(self, classification, attributes: List[Attribute]):
        self.attributes = attributes
        self.classification = classification

    def getAttributeWithDefinition(self, attributeDefinition: AttributeDefinition):
        for attr in self.attributes:
            if attr.attributeDefinition.id == attributeDefinition.id:
                return attr
