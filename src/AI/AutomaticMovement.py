from src.entities.Entity import Entity
from src.entities.Player import Movement
from queue import PriorityQueue


class AutomaticMovement:

    def __init__(self, player, gameMap):
        self.map = gameMap
        self.player = player
        self.nextMove = None
        self.movesList = None
        self.actualTarget = None

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


class node:
    def __init__(self, parent, action):
        self.parent = parent
        self.action = action
