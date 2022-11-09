# todo because aquarium will be initializing fish should we have "attribute randomizer with limit" method in that class
# todo instead of timer we could say a fish with a higher speed gets x more moves to every 1 move of a slower fish?
class Fish:

    # constant variables that will not change
    #for termination state
    ALIVE = 1
    DEAD = 0
    #for movements (row, col)
    UP = (0, 1)
    DOWN = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    NORTHEAST = tuple(map(sum, zip(UP, RIGHT)))
    NORTHWEST = tuple(map(sum, zip(UP, LEFT)))
    SOUTHEAST = tuple(map(sum, zip(DOWN, RIGHT)))
    SOUTHWEST = tuple(map(sum, zip(DOWN, LEFT)))

    # all fish will have various attributes (initialized by aquarium class)
    def __init__(self, loc, vision, speed, riskTolerance):
        self.loc = loc
        self.vision = vision
        self.speed = speed
        self.riskTolerance = riskTolerance
        self.status = self.ALIVE
        self.score = 0
        self.movementQueue = self.path() #a list movements for a path fish will take (A* for training fish, pre-defined for non-training fish)

    #in our aquarium we will have a loop that calls this method for every fish present (held in stack) to update their location
    def getMove(self):
        if (len(self.movementQueue) > 0):
            move = self.movementQueue.pop(0)
            self.updateLoc(move)

    def translateMove(self, curLoc, delta):
        return tuple(map(sum, zip(curLoc, delta)))

    #A*
    def path(self):
        pass

    # # all fish will have a update method (in which their location is changed if that fish is moving, else it stays the same)
    # # move direction is a tuple
    # def updateLoc(self, moveDirection):
    #
    #     if moveDirection == self.UP:
    #         delta = self.UP
    #     elif moveDirection == self.DOWN:
    #         delta = self.DOWN
    #     elif moveDirection == self.RIGHT:
    #         delta = self.RIGHT
    #     elif moveDirection == self.LEFT:
    #         delta = self.LEFT
    #     elif moveDirection == self.NORTHEAST:
    #         delta = self.NORTHEAST
    #     elif moveDirection == self.NORTHWEST:
    #         delta = self.NORTHWEST
    #     elif moveDirection == self.SOUTHEAST:
    #         delta = self.SOUTHEAST
    #     elif moveDirection == self.SOUTHWEST:
    #         delta = self.SOUTHWEST
    #     else:
    #         delta = "fail"
    #         print("Fish Parent Class Error -> no valid move direction passed to updateLoc")
    #         quit()
    #
    #     self.loc = self.translateMove(self.loc, delta)