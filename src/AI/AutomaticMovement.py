from src.entities.Entity import Entity
from entities.Enums import Rotations, Movement
from src.entities.Interactable import Interactable
from src.entities.Pickupable import Pickupable
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
        # A flag to set if the player should do a pick up action
        self.canPickup = False

    def pickUp(self):
        object = self.map.getEntityOnCoord(self.player.getFacingCoord())
        # Picked up item gets removed from the map
        if type(object) is Pickupable:
            object.on_interaction(self.player)
            self.map.removeSpriteFromMap(object)
        elif type(object) is Interactable:
            object.on_interaction(self.player)

    def gotoToTarget(self, target: Entity):
        if self.actualTarget is None:
            self.actualTarget = target
            self.targetCoords = (self.actualTarget.rect.x - self.leftUiWidth, self.actualTarget.rect.y)
            self.movesList = self.a_Star()
            if self.movesList is not None:
                if len(self.movesList) > 0:
                    self.nextMove = self.movesList[0]
                else:
                    self.actualTarget = None
                    self.nextMove = None
            else:
                self.actualTarget = None

    def updatePlayerCoords(self):
        if self.actualTarget is not None and self.nextMove is not None:
            if self.player.move(self.nextMove):
                self.movesList.remove(self.nextMove)
                if len(self.movesList) != 0:
                    self.nextMove = self.movesList[0]
                else:
                    if self.canPickup:
                        self.pickUp()
                        self.canPickup = False
                    self.movesList = None
                    self.nextMove = None
                    self.actualTarget = None

    def a_Star(self):
        print("A* in progress ...")

        self.testCount = 0

        fringe = PriorityQueue()
        explored = []

        startingState = (self.player.rect.x - self.leftUiWidth, self.player.rect.y, self.player.rotation)
        startingPriority = 0

        fringe.put((startingPriority, self.testCount, AStarNode(None, None, startingState)))
        self.testCount += 1
        while True:
            if fringe.empty():
                # target is unreachable
                print("PATH NOT FOUND")
                return None

            elem: AStarNode = fringe.get()[2]

            # After completing the algorithm, the player may pick up an item at the destination
            self.canPickup = True

            if self.goalTest(elem.state):
                print("PATH FOUND")
                movesList = []

                if isinstance(self.actualTarget, Entity) or self.actualTarget in self.map.collidables:
                    elem = elem.parent

                while elem.action is not None:
                    movesList.append(elem.action)
                    elem = elem.parent

                movesList.reverse()
                return movesList

            # debug
            print("DEBUG")
            print("ACTUAL STATE: {}".format(elem.state))
            print("HOW TO GET HERE:")
            temp = elem
            while temp.action is not None:
                print(temp.action)
                temp = temp.parent

            print("POSSIBLE MOVEMENTS FROM HERE:")
            for el in self.succesor(elem.state):
                print(el)

            print("*" * 20)

            explored.append(elem)

            for (movement, newState) in self.succesor(elem.state):
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
        if 0 <= stateAfterForward[0] <= self.map.width and 0 <= stateAfterForward[1] <= self.map.height:
            coordsWithUiOffset = [stateAfterForward[0] + self.leftUiWidth, stateAfterForward[1]]
            facingEntity = self.map.getEntityOnCoord(coordsWithUiOffset)

            if facingEntity is not None:
                if isinstance(self.actualTarget, Entity):
                    if facingEntity.id == self.actualTarget.id:
                        result.append((Movement.FORWARD, stateAfterForward))
            elif self.map.collision(coordsWithUiOffset[0], coordsWithUiOffset[1]) and \
                    self.targetCoords[0] == stateAfterForward[0] and self.targetCoords[1] == stateAfterForward[1]:
                result.append((Movement.FORWARD, stateAfterForward))
            elif not self.map.collision(coordsWithUiOffset[0], coordsWithUiOffset[1]):
                result.append((Movement.FORWARD, stateAfterForward))

        return result

    def goalTest(self, coords):
        if coords[0] == self.targetCoords[0] and coords[1] == self.targetCoords[1]:
            return True
        return False

    def approximateDistanceFromTarget(self, tileX, tileY):
        return abs(tileX - self.targetCoords[0]) + abs(tileY - self.targetCoords[1])

    def stepCost(self, terrainTile: TerrainTile):

        # TODO: Nie znajduje terraina na ktorym stoi player
        if terrainTile is None:
            return 1000
        return terrainTile.cost

    def priority(self, elem: AStarNode):
        coordsWithUiOffset = [elem.state[0] + self.leftUiWidth, elem.state[1]]
        return self.approximateDistanceFromTarget(elem.state[0], elem.state[1]) + self.stepCost(
            self.map.getTileOnCoord(coordsWithUiOffset))

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


# As non-objective


def newStateAfterAction(movable, state, action: Movement):
    """
    Returns a state after a given action
    :type movable: Entity
    :param movable: Movable entity
    :param state: Current entity state
    :param action: What did entity do
    :return: A tuple of (x, y, rotation)
    """
    newX = state[0]
    newY = state[1]
    newRotation = state[2]

    if action == Movement.FORWARD:
        if state[2] == Rotations.NORTH:
            newY -= movable.rect.w
        elif state[2] == Rotations.EAST:
            newX += movable.rect.w
        elif state[2] == Rotations.SOUTH:
            newY += movable.rect.w
        elif state[2] == Rotations.WEST:
            newX -= movable.rect.w
    elif action == Movement.ROTATE_L:
        newRotation = Rotations((state[2].value - 1) % 4)
    elif action == Movement.ROTATE_R:
        newRotation = Rotations((state[2].value + 1) % 4)

    newState = (newX, newY, newRotation)

    return newState


def stepCost(terrainTile: TerrainTile):
    """
    Gets the cost of a given tile
    :param terrainTile:
    :return: Step cost as int
    """
    if terrainTile is None:
        return 1000
    return terrainTile.cost


def approximateDistanceFromTarget(tileX, tileY, target):
    """
    Given X, Y and a target, approximate the distance.
    :param tileX: X coord
    :param tileY: Y coord
    :param target: Target entity
    :return: Distance as int
    """
    return abs(tileX - target.rect.x) + abs(tileY - target.rect.y)


def priority(elem: AStarNode, map, target):
    """
    Gets the priority of the move.
    :param elem: Node
    :param map: Map object
    :param target: Target goal
    :return: Priority as int
    """
    return approximateDistanceFromTarget(elem.state[0], elem.state[1], target) + stepCost(
        map.getTileOnCoord((elem.state[0], elem.state[1])))


def successor(movable: Entity, elemState, map, target):
    """
    Successor function for a given movable object (Usually a player)
    :type target: Entity
    :param target:
    :param elemState: [x, y, Rotation]
    :return: list of (Movement, NewState)
    """
    result = [(Movement.ROTATE_R, newStateAfterAction(movable, elemState, Movement.ROTATE_R)),
              (Movement.ROTATE_L, newStateAfterAction(movable, elemState, Movement.ROTATE_L))]

    stateAfterForward = newStateAfterAction(movable, elemState, Movement.FORWARD)
    # if 0 <= stateAfterForward[0] <= map.width and 0 <= stateAfterForward[1] <= map.height:
    if True:
        facingEntity = map.getEntityOnCoord((stateAfterForward[0], stateAfterForward[1]))

        if facingEntity is not None:
            if isinstance(target, Entity):
                if facingEntity.id == target.id:
                    result.append((Movement.FORWARD, stateAfterForward))
        elif map.collision(stateAfterForward[0], stateAfterForward[1]) and \
                target.rect.x == stateAfterForward[0] and target.rect.y == stateAfterForward[1]:
            result.append((Movement.FORWARD, stateAfterForward))
        elif not map.collision(stateAfterForward[0], stateAfterForward[1]):
            result.append((Movement.FORWARD, stateAfterForward))

        return result


def goalTest(coords, target):
    """
    Check whether the target has been reached.
    :param coords: A tuple of X and Y coords
    :param target: Target
    :return: True, if the goal is reached
    """
    if coords[0] == target.rect.x and coords[1] == target.rect.y:
        return True
    return False


def aStar(movable: Entity, target, map):
    """
    A* pathfinder function. Composes an array of moves to do in order to reach a target.
    :param movable: An entity to move (Usually a player)
    :param target: Target object
    :param map: Map object
    :return: Array of moves
    """
    testCount = 0

    fringe = PriorityQueue()
    explored = []

    startingState = (movable.rect.x, movable.rect.y, movable.rotation)
    startingPriority = 0

    fringe.put((startingPriority, testCount, AStarNode(None, None, startingState)))
    testCount += 1
    while True:
        if fringe.empty():
            # target is unreachable
            print("PATH NOT FOUND")
            return None

        elem: AStarNode = fringe.get()[2]

        if goalTest(elem.state, target):
            print("PATH FOUND")
            movesList = []

            if isinstance(target, Entity) or target in map.collidables:
                elem = elem.parent

            while elem.action is not None:
                movesList.append(elem.action)
                elem = elem.parent

            movesList.reverse()
            return movesList

        # debug
        # print("DEBUG")
        print("ACTUAL STATE: {}".format(elem.state))
        print("HOW TO GET HERE:")
        temp = elem
        while temp.action is not None:
            print(temp.action)
            temp = temp.parent
        #
        # print("POSSIBLE MOVEMENTS FROM HERE:")
        # for el in self.successor(elem.state):
        #     print(el)
        #
        # print("*" * 20)

        explored.append(elem)

        for (movement, newState) in successor(movable, elem.state, map, target):
            newNode = AStarNode(elem, movement, newState)
            newPriority = priority(newNode, map, target)

            # Check if state is not in fringe queue ... # ... and is not in explored list
            if not any(newNode.state == node[2].state for node in fringe.queue) \
                    and not any(newNode.state == node.state for node in explored):
                # there can't be nodes with same priority
                fringe.put((newPriority, testCount, newNode))
                testCount += 1
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
                            testCount += 1
                            break
