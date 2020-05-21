from typing import List

from src.AI.DecisionTrees.AttributeDefinition import AttributeDefinition
from src.AI.DecisionTrees.DecisionTreeBranch import DecisionTreeBranch
from src.AI.DecisionTrees.DecisionTreeExample import DecisionTreeExample


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

    def giveAnswer(self, example: DecisionTreeExample):
        if self.branchesNum == 0:
            return self.root

        for attr in example.attributes:
            if attr.attributeDefinition.id == self.root.id:
                for branch in self.branches:
                    if branch.label == attr.value:
                        return branch.subtree.giveAnswer(example)
