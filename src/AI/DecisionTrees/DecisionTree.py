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

    @staticmethod
    def printTree(tree, depth: int, indent: int = 50):
        if isinstance(tree.root, AttributeDefinition):
            print("NODE: {}".format(tree.root.name).rjust(indent * depth))
        else:
            print("NODE: {}".format(str(tree.root)).rjust(indent * depth))

        for branch in tree.branches:
            print("| {}".format(str(branch.label)).rjust(indent * depth))
            DecisionTree.printTree(branch.subtree, depth + 1, indent)
