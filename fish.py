# todo because aquarium will be initializing fish should we have "attribute randomizer with limit" method in that class
# todo instead of timer we could say a fish with a higher speed gets x more moves to every 1 move of a slower fish?
import random


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
    def __init__(self, loc, vision, speed, riskAwareness, movementPattern=None):
        self.loc = loc
        self.vision = vision
        self.speed = speed
        self.riskAwareness = riskAwareness
        self.status = self.ALIVE
        self.score = 0

        if (movementPattern == None):
            self.movementQueue = self.path()
        else:
            self.movementQueue = movementPattern

    # in our aquarium we will have a loop that calls this method for every fish present (held in stack) to update their location
    def getMove(self, visionGrid):

        # todo add an interpretation for visionGrid
        # check if current grid interferes with current path (present in movementQueue)

        if (len(self.movementQueue) > 0):
            move = self.movementQueue.pop(0)
            return self.myDest(move)
        return self.loc

    def translateMove(self, curLoc, delta):
        print("Fish Destination: ", tuple(map(sum, zip(curLoc, delta))))
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

    def aSearch(self, visionGrid):
        pass

    def findAdjacencies(self, loc, visionGrid):
        width = len(visionGrid)
        height = len(visionGrid[0])
        allDirections = [self.UP, self.DOWN, self.LEFT, self.RIGHT, self.NORTHEAST, self.NORTHWEST, self.SOUTHEAST, self.SOUTHWEST]
        adjacencies = list()
        for direction in allDirections:
            adjacent = self.translateMove(loc, direction)
            if(adjacent[0] >= 0 and adjacent[0] < width and adjacent[1] >= 0 and adjacent[1] < height):
                adjacencies.append(adjacent)
        return adjacencies

    @staticmethod
    def randomFishGenerator(loc):
        vision = 0
        speed = 0
        riskAwareness = 0
        for i in range(15):
            r = random.randint(0, 2)
            if r == 0:
                vision += 1
            elif r == 1:
                speed += 1
            else:
                riskAwareness += 1
        return Fish(loc, vision, speed, riskAwareness)

    def __repr__(self):
<<<<<<< HEAD
        return "fish"
=======
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

>>>>>>> ec4080daf5b5de3cf32b928fa692bc4d43460a40
