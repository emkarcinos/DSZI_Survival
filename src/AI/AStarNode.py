class AStarNode:
    def __init__(self, parent, action, state):
        self.state = state
        self.parent = parent
        self.action = action