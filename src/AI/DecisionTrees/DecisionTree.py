from typing import List, Any

from src.AI.DecisionTrees.AttributeDefinition import AttributeDefinition


class DecisionTree(object):
    root: AttributeDefinition
    branches: List[Any]

    def __init__(self, root):
        self.root = root
        self.branches = []
        self.branchesNum = 0