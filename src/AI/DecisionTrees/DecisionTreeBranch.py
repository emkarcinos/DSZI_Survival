from src.AI.DecisionTrees.DecisionTree import DecisionTree


class DecisionTreeBranch(object):
    subtree: DecisionTree

    def __init__(self, parent, label, subtree):
        self.subtree = subtree
        self.label = label
        self.parent = parent
