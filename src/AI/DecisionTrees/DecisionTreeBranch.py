class DecisionTreeBranch(object):

    def __init__(self, parent, label, subtree):
        self.subtree = subtree
        self.label = label
        self.parent = parent
