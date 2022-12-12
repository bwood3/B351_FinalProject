from aquarium import Aquarium
from fish import Fish
from evolution import Evolution
from PyAquarium.PyView import View
import random
from csv import writer

def runPySim():
    print("Running Main Pygame")
    gridSize = 20 # this can be viewed as equivalent to pixel count
    displaySize = 750
    view = View(gridSize, displaySize)

def runConsoleSim(n, collectData = False):
    print("Running Main Console")

    # FOR COLLECTING DATA IN CSV FILE ONLY
    if(collectData):
        initCSV()

    origin = (10, 10)  # starting point for the training fish
    mutationChance = 0.02
    maxAttributePoints = 15
    #locations that our fish may spawn
    possibleX = [1, 3, 5, 7, 13, 15, 17, 19]
    possibleY = [1, 3, 5, 7, 13, 15, 17, 19]
    evolution = Evolution(mutationChance, origin, maxAttributePoints)
    training_fishes = [Fish.randomFishGenerator(origin, "training", maxAttributePoints) for i in range(10)]
    generation = 0
    while(generation < n):
        scores = []
        bestFish = None
        bestScore = -1
        for i in training_fishes:
            fishes = []
            for j in range(0, 9):
                x = random.randint(0, 7)
                y = random.randint(0, 7)
                loc = (possibleX[x], possibleY[y])
                f = Fish.randomFishGenerator(loc, "npc", maxAttributePoints)
                fishes.append(f)
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            loc = (possibleX[x], possibleY[y])
            f = Fish(loc, 2, 2, 0, 20, "npc") #adds a predator npc
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
        generation+= 1

        print("Best fish had: " + bestFish.strAttributes())
        print("With score: " + str(bestScore))
        #print(scores)
        print("Average: " + str(sum(scores) / 10))
        training_fishes = evolution.createGeneration(training_fishes)

        # for collecting data into csv file only
        if(collectData):
            captureData(bestFish, str(bestScore), str(sum(scores) / 10))
    print("Sim over")

def initCSV():
    print("COLLECTING CSV DAT:\n\t*if you want to collect data into CSV press enter\n\t*else comment out code in ConsoleSim")
    input()
    header = ["Score", "Vision", "Speed", "Risk", "Tier", "Average"]
    with open('MUTATION_DATA.csv', 'w+') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(header)
        f_object.close()

def captureData(bestFish, bestScore, average):
    #new row
    data = [bestScore, bestFish.vision, bestFish.speed, bestFish.riskAwareness, bestFish.initTier, average]
    with open('MUTATION_DATA.csv', 'a') as f_object:
        writer_object  = writer(f_object)
        writer_object.writerow(data)
        f_object.close()


if __name__ == '__main__':
    # argument is # of generations
    # runConsoleSim(30)
    runPySim()


