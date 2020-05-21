from typing import List, Any

from src.AI.DecisionTrees.AttributeDefinition import AttributeDefinition
from src.AI.DecisionTrees.DecisionTreeBranch import DecisionTreeBranch


class DecisionTree(object):
    root: AttributeDefinition
    branches: List[DecisionTreeBranch]

    def __init__(self, root):
        self.root = root
        self.branches = []
        self.branchesNum = 0

    def addBranch(self, newBranch):
        self.branches.append(newBranch)
        self.branchesNum += 1
