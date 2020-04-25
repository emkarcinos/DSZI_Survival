from copy import copy

from src.entities.Entity import Entity
from src.entities.Player import Movement, Rotations
from queue import PriorityQueue


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
        # todo: A*!!!
        fringe = PriorityQueue()
        explored = []

        startingPos = (self.player.x, self.player.y, self.player.rotation.value)
        startingPriority = 0

        fringe.put((startingPriority, node(None, None)))
        while True:
            if fringe.empty():
                # target is unreachable
                self.movesList = None
                self.nextMove = None

            elem = fringe.get()

            if self.goalTest():
                # TODO : listaRuchow
                return None


        self.movesList = fringe
        self.nextMove = self.fringe[0]


    def succesor(self):
        movesList = [Movement.ROTATE_L, Movement.ROTATE_R]

        # Check if can move forward
        facingCoord = self.player.getFacingCoord()
        facingEntity = self.map.getEntityOnCoord(facingCoord)
        if facingEntity is not None:
            movesList.append(Movement.FORWARD)

        return movesList

    def goalTest(self, coords):
        entity = self.map.getEntityOnCoord(coords)

        if entity.id == self.actualTarget.id:
            return True

        return False

    def approximateDistanceFromTarget(self, nextTileX, nextTileY):
        return abs(nextTileX - self.actualTarget.x) + abs(nextTileY - self.actualTarget.y)

    def stepCost(self, destinationTile):
        # TODO : w oparciu o koszt danej kratki
        return 1

    def priority(self, apprDist, stepCost):
        return apprDist + stepCost


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


class node:
    def __init__(self, parent, action):
        self.parent = parent
        self.action = action
