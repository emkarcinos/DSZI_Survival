from copy import copy

from src.entities.Entity import Entity
from src.entities.Player import Movement, Rotations
from src.AI.AStarNode import AStarNode
from queue import PriorityQueue

from src.game.TerrainTile import TerrainTile


class AutomaticMovement:

    def __init__(self, player, gameMap, leftUiWidth):
        self.map = gameMap
        self.player = player
        self.nextMove = None
        self.movesList = None
        self.actualTarget = None
        self.moveOffset = self.player.rect.w
        self.leftUiWidth = leftUiWidth
        self.targetCoords = None

        self.testCount = 0

    def gotoToTarget(self, target: Entity):
        if self.actualTarget is None:
            self.actualTarget = target
            self.targetCoords = (self.actualTarget.rect.x - self.leftUiWidth, self.actualTarget.rect.y)
            self.movesList = self.a_Star()
            if self.movesList is not None:
                self.nextMove = self.movesList[0]
            else:
                self.actualTarget = None

    def updatePlayerCoords(self):
        if self.actualTarget is not None:
            self.player.move(self.nextMove)
            self.movesList.remove(self.nextMove)
            if len(self.movesList) != 0:
                self.nextMove = self.movesList[0]
            else:
                self.nextMove = None
                self.actualTarget = None

    def a_Star(self):
        self.testCount = 0

        fringe = PriorityQueue()
        explored = []

        startingState = (self.player.rect.x - self.leftUiWidth, self.player.rect.y, self.player.rotation)
        startingPriority = 0



        fringe.put((startingPriority, self.testCount, AStarNode(None, None, startingState)))
        self.testCount += 1
        while True:
            print("DEBUG: A* in progress")



            if fringe.empty():
                # target is unreachable
                self.movesList = None
                self.nextMove = None
                print("PATH NOT FOUND")
                return None

            elem: AStarNode = fringe.get()[2]

            if self.goalTest(elem.state):
                movesList = []
                while elem.action is not None:
                    movesList.append(elem.action)
                    elem = elem.parent

                movesList.reverse()
                return movesList

            explored.append(elem)

            for (movement, newState) in self.succesor(elem.state):
                # Sprawdzam czy nie jest poza mapa
                coordsWithUiOffset = [newState[0] + self.leftUiWidth, newState[1]]

                if 0 <= newState[0] <= self.map.width - self.moveOffset and 0 <= newState[1] <= self.map.height - self.moveOffset:
                #if self.map.getTileOnCoord(coordsWithUiOffset) is not None:
                    newNode = AStarNode(elem, movement, newState)
                    newPriority = self.priority(newNode)

                    # Check if state is not in fringe queue ... # ... and is not in explored list
                    if not any(newNode.state == node[2].state for node in fringe.queue) \
                            and not any(newNode.state == node.state for node in explored):
                        # there can't be nodes with same priority
                        fringe.put((newPriority, self.testCount, newNode))
                        self.testCount += 1
                    # If state is in fringe queue ...
                    elif any(newNode.state == node[2].state for node in fringe.queue):
                        node: AStarNode
                        for (pr, count, node) in fringe.queue:
                            # Compare nodes
                            if node.state == newNode.state and node.action == newNode.action:
                                # ... and if it has priority > newPriority
                                if pr > newPriority:
                                    # Replace it with new priority
                                    fringe.queue.remove((pr, count, node))
                                    fringe.put((newPriority, count, node))
                                    self.testCount += 1
                                    break

    def succesor(self, elemState):
        '''
        :param elemState: [x, y, Rotation]
        :return: list of (Movement, NewState)
        '''
        result = [(Movement.ROTATE_R, self.newStateAfterAction(elemState, Movement.ROTATE_R)),
                  (Movement.ROTATE_L, self.newStateAfterAction(elemState, Movement.ROTATE_L))]

        stateAfterForward = self.newStateAfterAction(elemState, Movement.FORWARD)
        if 0 <= stateAfterForward[0] <= self.map.width - self.moveOffset and 0 <= stateAfterForward[1] <= self.map.height - self.moveOffset:
            coordsWithUiOffset = [stateAfterForward[0] + self.leftUiWidth, stateAfterForward[1]]
            #facingEntity = self.map.getEntityOnCoord(coordsWithUiOffset)    # TU JEST BLAD BO U CELU JEST ZAWSZE JAKIES ENTITY
            facingEntity = None
            if facingEntity is None:
                result.append((Movement.FORWARD, stateAfterForward))

        return result

    def goalTest(self, coords):

        # with left ui width
        coordsWithUiOffset = [coords[0] + self.leftUiWidth, coords[1]]
        entity = self.map.getEntityOnCoord(coordsWithUiOffset)
        '''if entity is not None:
            if entity.id == self.actualTarget.id:
                return True'''

        if coords[0] == self.targetCoords[0] and coords[1] == self.targetCoords[1]:
            return True

        return False

    def approximateDistanceFromTarget(self, tileX, tileY):
        return abs(tileX - self.targetCoords[0]) + abs(tileY - self.targetCoords[1])

    def stepCost(self, terrainTile: TerrainTile):

        # TODO: Nie znajduje terraina na ktorym stoi player
        if terrainTile is None:
            return 0
        #return terrainTile.cost
        return 0

    def priority(self, elem: AStarNode):
        coordsWithUiOffset = [elem.state[0] + self.leftUiWidth, elem.state[1]]
        return self.approximateDistanceFromTarget(elem.state[0], elem.state[1]) + self.stepCost(self.map.getTileOnCoord(coordsWithUiOffset))

    '''
    state[0] - x
    state[1] - y
    state[2] - rotation
    '''

    def newStateAfterAction(self, state, action: Movement):

        newX = state[0]
        newY = state[1]
        newRotation = state[2]

        if action == Movement.FORWARD:
            if state[2] == Rotations.NORTH:
                newY -= self.moveOffset
            elif state[2] == Rotations.EAST:
                newX += self.moveOffset
            elif state[2] == Rotations.SOUTH:
                newY += self.moveOffset
            elif state[2] == Rotations.WEST:
                newX -= self.moveOffset
        elif action == Movement.ROTATE_L:
            newRotation = Rotations((state[2].value - 1) % 4)
        elif action == Movement.ROTATE_R:
            newRotation = Rotations((state[2].value + 1) % 4)


        newState = (newX, newY, newRotation)

        return newState
