from src.AI.DecisionTrees.AttributeDefinition import AttributeDefinition


class Attribute:
    def __init__(self, attributeDefinition: AttributeDefinition, value):
        self.attributeDefinition = attributeDefinition
        self.value = value
