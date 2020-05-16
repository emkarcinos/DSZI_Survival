from src.entities.Entity import Entity
from src.entities.Enums import Rotations, Movement
from src.AI.AStarNode import AStarNode
from queue import PriorityQueue

from src.game.TerrainTile import TerrainTile


def newStateAfterAction(movable, state, action: Movement):
    """
    Returns a state after a given action

    :type movable: Entity
    :param movable: Movable entity
    :param state: Current entity state (x, y, rotation). Coords are relative
    :param action: What did entity do
    :return: A tuple of (x, y, rotation)
    """
    newX = state[0]
    newY = state[1]
    newRotation = state[2]

    if action == Movement.FORWARD:
        if state[2] == Rotations.NORTH:
            newY -= 1
        elif state[2] == Rotations.EAST:
            newX += 1
        elif state[2] == Rotations.SOUTH:
            newY += 1
        elif state[2] == Rotations.WEST:
            newX -= 1
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
    Given relative X, Y and a target, approximate the distance.

    :param tileX: relative X coord
    :param tileY: relative Y coord
    :param target: Target entity
    :return: Distance as int
    """
    return abs(tileX - target.x) + abs(tileY - target.y)


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
    :param elemState: [x, y, Rotation]. x, y are relative
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
                target.x == stateAfterForward[0] and target.y == stateAfterForward[1]:
            result.append((Movement.FORWARD, stateAfterForward))
        elif not map.collision(stateAfterForward[0], stateAfterForward[1]):
            result.append((Movement.FORWARD, stateAfterForward))

        return result


def goalTest(coords, target):
    """
    Check whether the target has been reached.

    :param coords: A tuple of X and Y coords (relative)
    :param target: Target
    :return: True, if the goal is reached
    """
    if coords[0] == target.x and coords[1] == target.y:
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
    # print("Finding path to x:", target.x, " y:", target.y, end='...\n')
    fringe = PriorityQueue()
    explored = []

    startingState = (movable.x, movable.y, movable.rotation)
    startingPriority = 0

    fringe.put((startingPriority, testCount, AStarNode(None, None, startingState)))
    testCount += 1
    while True:
        if fringe.empty():
            # target is unreachable
            # print("Couldn't find path to x:", target.x, " y:", target.y, end='.\n')
            return None

        elem: AStarNode = fringe.get()[2]

        if goalTest(elem.state, target):
            # print("Found path to x:", target.x, " y:", target.y, end='.\n')
            movesList = []

            if isinstance(target, Entity) or target in map.collidables:
                elem = elem.parent

            while elem.action is not None:
                movesList.append(elem.action)
                elem = elem.parent

            movesList.reverse()
            return movesList

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
