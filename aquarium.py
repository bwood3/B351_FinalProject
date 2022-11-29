import random
from fish import Fish

class Aquarium:

    def __init__(self, size, fishes):
        self.size = size #Size N of the NxN grid
        self.fishes = fishes #contains all fish, living and dead
        self.grid = self.createGrid(size, fishes) #contains living fish at their respective locations
        self.lifetime = 0 #how long the aquarium has been simulating
        
    #Used to create a new N*N grid of the given size,
    #then inserts the list of fish into their respective location
    def createGrid(self, size, fishes):
        grid = [ [ list() for y in range(0, size)] for x in range(0, size)]
        for fish in fishes:
            x, y = fish.loc
            grid[x][y].append(fish)
        return grid

    #prints a representation of the grid
    def __repr__(self):
        string = ""
        for y in range(0, self.size):
            for x in range(0, self.size):
                if self.grid[x][y] == []:
                    string += "[ " + "] "
                else:
                    string += "" + ''.join(str(self.grid[x][y])) + " "
                if x == self.size - 1:
                    print(string)
                    string = ""
        return string

    #checks for overlapping fish on a given node. The largest tiered fish will
    #eat all the others. This currently does not rechecked what fish can be eaten
    #if the predator fish grows in size, thus may be eligible to eat other fish 
    #that were once the same size as it.
    #node is a tuple of integers in order (x, y)
    def checkOverlap(self, node):
        fishAtNode = list(self.grid[node[0]][node[1]])
        maxTier = -1
        for fish in fishAtNode:
            if fish.getTier() > maxTier:
                predator = fish
                maxTier = fish.getTier()
        for fish in list(fishAtNode):
            if fish.getTier() == maxTier and not fish.fishType == "food":
                fishAtNode.remove(fish)
        for fish in fishAtNode:
            sustanence = max(10, fish.score)
            predator.score += sustanence
            fish.status = 0
            self.grid[node[0]][node[1]].remove(fish)

    #returns the euclidean disntace between two nodes
    def calc_euclidean_distance(self, node_a, node_b):
        distance = 0
        for a, b in zip(node_a, node_b):
            distance += pow(a - b, 2)
        distance = pow(distance, 0.5)
        return distance   
            
    #return a copy of the grid with only what the fish can see
    def getVision(self, fish):
        visionRange = fish.vision #this is the integer value of how far the fish can see
        visibleFish = []
        for otherFish in self.fishes:
            distance = self.calc_euclidean_distance(fish.loc, otherFish.loc)
            if visionRange >= distance:
                visibleFish.append(otherFish)
        limitedGrid = self.createGrid(self.size, visibleFish)
        return limitedGrid, visibleFish

    #checks to make sure the destination node a fish trys to move to is valid
    def checkValidMove(self, destNode):
        x, y = destNode
        return (x >= 0 and x < self.size and y >= 0 and y < self.size)
            
    #finds the fishes visionGrid, gives it to the fish to make a move, then validates
    #and moves the fish to the destination node, before finally checking overlaps at
    #destination
    def moveFish(self, fish):
        visionGrid, visibleFish = self.getVision(fish)
        destNode = fish.getMove(visionGrid, visibleFish)
        if self.checkValidMove(destNode):
            oldPos = fish.loc
            fish.loc = destNode
            x, y = oldPos
            self.grid[x][y].remove(fish)
            x, y = destNode
            self.grid[x][y].append(fish)
            self.checkOverlap(destNode)

    #This is the function called by main for every tick of the simulation.
    #It updates all of the fish not dead.
    def updateSim(self):
        self.lifetime += 1
        maxSpeed = 0
        if (self.lifetime % 10) == 0:
            self.createFood()
        for fish in self.fishes:
            if fish.status:
                maxSpeed = max(maxSpeed, fish.speed)
        for i in range(maxSpeed, 0, -1):
            for fish in self.fishes:
                if fish.status and fish.speed >= i:
                    self.moveFish(fish)
        i = 0
        while i != len(self.fishes):
            fish = self.fishes[i]
            if not fish.status:
                self.fishes.remove(fish)
            else:
                i += 1


    def createFood(self):
        foodLoc = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        food = Fish(foodLoc, 0, 0, 0, 0, "food")
        self.fishes.append(food)
        self.grid[foodLoc[0]][foodLoc[1]].append(food)
        
