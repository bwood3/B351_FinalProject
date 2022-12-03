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

    # All fish will have various attributes which affect their performance and -
    # - place on the food chain (initTier).
    # All fish will be initialized using "randomFishGenerator" but training fish -
    # - will be cross breed via evolution class.
    # current fishType's include (training fish, npc, and food)
    def __init__(self, loc, vision, speed, riskAwareness, initTier, fishType):
        self.loc = loc
        self.vision = vision
        self.speed = speed
        # how close a fish is willing to get to a fish of a higher tier to secure a food source -
        # - note a fish of a higher tier is able to eat fish ending it's lifecycle
        self.riskAwareness = riskAwareness
        self.initTier = initTier
        self.status = self.ALIVE
        self.score = 0
        self.fishType = fishType

    def getTier(self):
        return math.floor(self.score / 10) + self.initTier

    def getMove(self, visionGrid, visibleFish):
        return self.startASearch(visionGrid, visibleFish)
        #return self.randomMove(visionGrid)

    def translateMove(self, curLoc, delta):
        return tuple(map(sum, zip(curLoc, delta)))

    def randomMove(self, visionGrid):
        adjacencies = self.findAdjacencies(self.loc, visionGrid)
        move = adjacencies[random.randint(0, len(adjacencies) - 1)]
        return move

    # returns a single move along a star search path
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
        # best moves (sorted via heapq)
        minFringe = []
        # max depth of any branch from root
        searchDepth = self.vision
        bestMoves = [Node(self.loc, 0, 100000)]
        heapq.heappush(minFringe, bestMoves[0])
        while (minFringe):
            parent = heapq.heappop(minFringe)
            if parent < bestMoves[0]:
                bestMoves = [parent]
            elif parent == bestMoves[0]:
                bestMoves.append(parent)

            # if we have not exceeded max depth from root
            if parent.depth <= searchDepth:
                for adj in self.findAdjacencies(parent.loc, visionGrid):
                    if not adj in parentMap.keys():
                        parentMap[adj] = parent.loc
                        heapq.heappush(minFringe,
                                       Node(adj, parent.depth + 1, self.heuristic(adj, visionGrid, visibleFish)))
        return bestMoves, parentMap

    def findAdjacencies(self, loc, visionGrid):
        # variables to prevent possible moves from going out of bounds
        width = len(visionGrid)
        height = len(visionGrid[0])
        allDirections = [self.UP, self.DOWN, self.LEFT, self.RIGHT, self.NORTHEAST, self.NORTHWEST, self.SOUTHEAST, self.SOUTHWEST, (0, 0)]
        adjacencies = list()
        for direction in allDirections:
            adjacent = self.translateMove(loc, direction)
            # prevent possible moves from going out of bounds
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
            # if our fish notices a fish of a higher tier and is within risk tolerance,
            if distance <= self.riskAwareness and otherFish.getTier() > self.getTier():
                if distance == 0:
                    value += (self.riskAwareness + 1)
                else:
                    value += (1 / distance) * self.riskAwareness
            elif (otherFish.getTier() < self.getTier() or otherFish.fishType == "food"):
                if distance == 0:
                    value -= (self.vision + 1)
                else:
                    value -= (1 / distance) * self.vision
        return value

    @staticmethod
    def randomFishGenerator(loc, fishType, totalPoints):
        attributes = [0, 0, 0, 0] #vision, speed, riskAwareness, initTier
        for i in range(totalPoints - 1):
            attributes[random.randint(0, 3)] += 1
        return Fish(loc, attributes[0], attributes[1], attributes[2], attributes[3], fishType)

    def __repr__(self):
        if self.fishType == "npc":
            return "N"
        if self.fishType == "training":
            return "T"
        if self.fishType == "food":
            return "F"
        return "fish"

    def strAttributes(self):
        return "Vision: "+ str(self.vision) + " Speed: " + str(self.speed) + " Risk: " + str(self.riskAwareness) + " Tier: " + str(self.initTier)

# Node class is used for A* implementation -> specifically node represents neighbor coordinates and has -
# - custom comparison methods to evaluate that neighbor coordinates goodness
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