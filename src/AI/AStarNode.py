class AStarNode:
    def __init__(self, parent, action, state):
        """
        Create a node used in A*.

        :type action: Rotations
        :param parent: Parent node
        :param action: Action (Rotation)
        :param state: A tuple of coords as (x,y,rotation)
        """
        self.state = state
        self.parent = parent
        self.action = action
