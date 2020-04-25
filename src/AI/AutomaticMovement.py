from copy import copy

from src.entities.Entity import Entity
from src.entities.Player import Movement, Rotations
from src.AI.AStarNode import AStarNode
from queue import PriorityQueue

from src.game.TerrainTile import TerrainTile


class AutomaticMovement:

    def __init__(self, player, gameMap):
        self.map = gameMap
        self.player = player
        self.nextMove = None
        self.movesList = None
        self.actualTarget = None
        self.moveOffset = self.player.rect.w

    def gotoToTarget(self, target: Entity):
        self.actualTarget = target

    def updatePlayerCoords(self):
        if self.actualTarget is not None:
            self.player.move(self.nextMove)
            self.movesList.remove(0)
            if len(self.movesList) != 0:
                self.nextMove = self.movesList[0]
            else:
                self.nextMove = None
                self.actualTarget = None

    def a_Star(self):
        fringe = PriorityQueue()
        explored = []

        startingState = (self.player.x, self.player.y, self.player.rotation)
        startingPriority = 0

        fringe.put((startingPriority, AStarNode(None, None, startingState)))
        while True:
            if fringe.empty():
                # target is unreachable
                self.movesList = None
                self.nextMove = None

            elem: AStarNode = fringe.get()

            if self.goalTest(elem.state):
                result = []
                p = elem.parent
                while p is not None:
                    result.append((elem.parent, elem.action))
                return result

            explored.append(elem)

            for (movement, newState) in self.succesor(elem.state):
                newNode = AStarNode(elem, movement, newState)
                newPriority = self.priority(newNode)

                # Check if state is not in fringe queue ...
                if not any(newNode.state == node[1].state for node in fringe.queue):
                    # ... and is not in explored list
                    if not any(newNode.state == node[1].state for node in explored):
                        fringe.put((newPriority, newNode))
                # If state is in fringe queue ...
                else:
                    node: AStarNode
                    for (pr, node) in fringe.queue:
                        # Compare nodes
                        if node.state == newNode.state and node.parent is newNode.parent and node.action == newNode.action:
                            # ... and if it has priority > newPriority
                            if pr > newPriority:
                                # Replace it with new priority
                                fringe.queue.remove((pr, node))
                                fringe.put((newPriority, node))

    def succesor(self, elemState):
        '''
        :param elemState: [x, y, Rotation]
        :return: list of (Movement, NewState)
        '''
        result = [(Movement.ROTATE_R, self.newStateAfterAction(elemState, Movement.ROTATE_R)),
                  (Movement.ROTATE_L, self.newStateAfterAction(elemState, Movement.ROTATE_L))]

        stateAfterForward = self.newStateAfterAction(elemState, Movement.FORWARD)
        facingEntity = self.map.getEntityOnCoord(stateAfterForward)

        if facingEntity is not None:
            result.append((Movement.FORWARD, stateAfterForward))

        return result

    def goalTest(self, coords):
        entity = self.map.getEntityOnCoord(coords)

        if entity.id == self.actualTarget.id:
            return True

        return False

    def approximateDistanceFromTarget(self, tileX, tileY):
        return abs(tileX - self.actualTarget.x) + abs(tileY - self.actualTarget.y)

    def stepCost(self, terrainTile: TerrainTile):
        return terrainTile.cost

    def priority(self, elem: AStarNode):
        return self.approximateDistanceFromTarget(elem.state[0], elem.state[1]) + self.stepCost(self.map.getTileOnCoord(elem.state))

    '''
    state[0] - x
    state[1] - y
    state[2] - rotation
    '''

    def newStateAfterAction(self, state, action: Movement):
        newState = copy(state)

        if action == Movement.FORWARD:
            if state[2] == Rotations.NORTH:
                newState[1] -= self.moveOffset
            elif state[2] == Rotations.EAST.value:
                newState[0] += self.moveOffset
            elif state[2] == Rotations.SOUTH.value:
                newState[1] += self.moveOffset
            elif state[2] == Rotations.WEST.value:
                newState[0] -= self.moveOffset
        elif action == Movement.ROTATE_L:
            newState[2] = Rotations((state[2] + 1) % 4)
        elif action == Movement.ROTATE_R:
            newState[2] = Rotations((state[2] - 1) % 4)

        return newState
