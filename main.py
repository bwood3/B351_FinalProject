from aquarium import Aquarium
from fish import Fish
from evolution import Evolution
from PyAquarium.PyView import View
import random

def runPySim():
    print("Running Main Pygame")
    gridSize = 20 # this can be viewed as equivalent to pixel count
    displaySize = 750
    view = View(gridSize, displaySize)

def runConsoleSim():
    print("Running Main Console")
    origin = (10, 10)  # starting point for the training fish
    mutationChance = 0.02
    maxAttributePoints = 15
    possibleX = [1, 3, 5, 7, 13, 15, 17, 19]
    possibleY = [1, 3, 5, 7, 13, 15, 17, 19]
    evolution = Evolution(mutationChance, origin, maxAttributePoints)
    training_fishes = [Fish.randomFishGenerator(origin, "training", maxAttributePoints) for i in range(10)]
    while(1):
        scores = []
        bestFish = None
        bestScore = -1
        for i in training_fishes:
            fishes = []
            for j in range(0, 10):
                x = random.randint(0, 7)
                y = random.randint(0, 7)
                loc = (possibleX[x], possibleY[y])
                f = Fish.randomFishGenerator(loc, "npc", maxAttributePoints)
                fishes.append(f)
            #i.score = 100
            fishes.append(i)
            aquarium = Aquarium(20, fishes)
            while aquarium.lifetime < 100 and i.status == 1:
                aquarium.updateSim()
                #print(aquarium)
            i.score += aquarium.lifetime
            scores.append(i.score)
            if(i.score > bestScore):
                bestFish = i
                bestScore = i.score
        print("Best fish had: " + bestFish.strAttributes())
        print("With score: " + str(bestScore))
        #print(scores)
        #print("Average: " + str(sum(scores) / 10))
        training_fishes = evolution.createGeneration(training_fishes)
    print("Run Demo:\n")

if __name__ == '__main__':
    runConsoleSim()
    # runPySim()


