# todo because aquarium will be initializing fish should we have "attribute randomizer with limit" method in that class
# todo instead of timer we could say a fish with a higher speed gets x more moves to every 1 move of a slower fish?
import random
import heapq
import math


class Fish:
    # constant variables that will not change
    # for termination state
    ALIVE = 1
    DEAD = 0
    # for movements (row, col)
    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    NORTHEAST = tuple(map(sum, zip(UP, RIGHT)))
    NORTHWEST = tuple(map(sum, zip(UP, LEFT)))
    SOUTHEAST = tuple(map(sum, zip(DOWN, RIGHT)))
    SOUTHWEST = tuple(map(sum, zip(DOWN, LEFT)))

    # all fish will have various attributes (initialized by aquarium class)
    # if we are using our training fish, movement pattern will be defined by A*
    # if we are not using training fish, it will be pre-defined as argument
    def __init__(self, loc, vision, speed, riskAwareness, fishType, movementPattern=None):
        self.loc = loc
        self.vision = vision
        self.speed = speed
        self.riskAwareness = riskAwareness
        self.status = self.ALIVE
        self.score = 0
        self.fishType = fishType

        if (movementPattern == None):
            self.movementQueue = self.path()
        else:
            self.movementQueue = movementPattern

    # in our aquarium we will have a loop that calls this method for every fish present (held in stack) to update their location
    def getMove(self, visionGrid, visibleFish):

        # todo add an interpretation for visionGrid
        # check if current grid interferes with current path (present in movementQueue)
        return self.startASearch(visionGrid, visibleFish)
        #return self.randomMove(visionGrid)

    def translateMove(self, curLoc, delta):
        return tuple(map(sum, zip(curLoc, delta)))

    # A list movements for a path training fish will take (A* for training fish, pre-defined for non-training fish)
    def path(self):
        return [self.UP, self.RIGHT, self.DOWN, self.NORTHEAST, self.NORTHEAST, self.SOUTHEAST, self.RIGHT,
                self.RIGHT]  # demo code

    # move direction is a tuple
    def myDest(self, moveDirection):

        if moveDirection == self.UP:
            delta = self.UP
        elif moveDirection == self.DOWN:
            delta = self.DOWN
        elif moveDirection == self.RIGHT:
            delta = self.RIGHT
        elif moveDirection == self.LEFT:
            delta = self.LEFT
        elif moveDirection == self.NORTHEAST:
            delta = self.NORTHEAST
        elif moveDirection == self.NORTHWEST:
            delta = self.NORTHWEST
        elif moveDirection == self.SOUTHEAST:
            delta = self.SOUTHEAST
        elif moveDirection == self.SOUTHWEST:
            delta = self.SOUTHWEST
        else:
            delta = "fail"
            print("Fish Class Error -> {0} is not a valid move direction".format(moveDirection))
            quit()

        return self.translateMove(self.loc, delta)

    def randomMove(self, visionGrid):
        adjacencies = self.findAdjacencies(self.loc, visionGrid)
        move = adjacencies[random.randint(0, len(adjacencies) - 1)]
        return move

    def startASearch(self, visionGrid, visibleFish):
        bestMoves, parentMap = self.aSearch(visionGrid, visibleFish)
        nextMoves = list()
        for move in bestMoves:
            parentMove = parentMap[move.loc]
            nextMove = move.loc
            while parentMove != self.loc:
                nextMove = parentMove
                parentMove = parentMap[parentMove]
            nextMoves.append(nextMove)
        choosenMove = nextMoves[random.randint(0, len(nextMoves) - 1)]
        return choosenMove

    def aSearch(self, visionGrid, visibleFish):
        parentMap = {}
        minFringe = []
        searchDepth = self.vision
        bestMoves = [Node(self.loc, 0, 100000)]
        heapq.heappush(minFringe, bestMoves[0])
        while(minFringe):
            parent = heapq.heappop(minFringe)
            if parent.value < bestMoves[0].value:
                bestMoves = [parent]
            elif parent.value == bestMoves[0].value:
                bestMoves.append(parent)
            if parent.depth <= searchDepth:
                for adj in self.findAdjacencies(parent.loc, visionGrid):
                    if not adj in parentMap.keys():
                        parentMap[adj] = parent.loc
                        heapq.heappush(minFringe, Node(adj, parent.depth + 1, self.heuristic(adj, visionGrid, visibleFish)))
        return bestMoves, parentMap

    def findAdjacencies(self, loc, visionGrid):
        width = len(visionGrid)
        height = len(visionGrid[0])
        allDirections = [self.UP, self.DOWN, self.LEFT, self.RIGHT, self.NORTHEAST, self.NORTHWEST, self.SOUTHEAST, self.SOUTHWEST, (0, 0)]
        adjacencies = list()
        for direction in allDirections:
            adjacent = self.translateMove(loc, direction)
            if (adjacent[0] >= 0 and adjacent[0] < width and adjacent[1] >= 0 and adjacent[1] < height):
                adjacencies.append(adjacent)
        return adjacencies

    def calc_euclidean_distance(self, node_a, node_b):
        distance = 0
        for a, b in zip(node_a, node_b):
            distance += pow(a - b, 2)
        distance = pow(distance, 0.5)
        return distance  

    def heuristic(self, loc, visionGrid, visibleFish):
        value = 0
        for otherFish in visibleFish:
            distance = self.calc_euclidean_distance(loc, otherFish.loc)
            if distance <= self.riskAwareness and otherFish.score > self.score and distance != 0:
                value += (1 / distance) * self.riskAwareness
            elif otherFish.score < self.score and distance != 0:
                value -= (1 / distance) * self.vision
        return value

    @staticmethod
    def randomFishGenerator(loc, fishType):
        vision = 0
        speed = 0
        riskAwareness = 0
        for i in range(9):
            r = random.randint(0, 2)
            if r == 0:
                vision += 1
            elif r == 1:
                speed += 1
            else:
                riskAwareness += 1
        return Fish(loc, vision, speed, riskAwareness, fishType)

    def __repr__(self):
        if self.fishType == "npc":
            return "N"
        if self.fishType == "training":
            return "T"
        if self.fishType == "food":
            return "F"
        return "fish"


class Node:

    def __init__(self, loc, depth, heuristicValue):
        self.loc = loc
        self.depth = depth
        self.value = heuristicValue

    def _is_valid_operand(self, other):
        return (hasattr(other, "depth") and
                hasattr(other, "value"))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.depth + self.value) == (other.depth + other.value)

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.depth + self.value) < (other.depth + other.value)

    def __gt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.depth + self.value) > (other.depth + other.value)

    def __le__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.depth + self.value) <= (other.depth + other.value)

    def __ge__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.depth + self.value) >= (other.depth + other.value)
