from aquarium import Aquarium
from fish import Fish
import random
if __name__ == '__main__':
    print("Running Main")
    origin = (10, 10)  # starting point for the training fish
    possibleX = [1, 3, 5, 7, 13, 15, 17, 19]
    possibleY = [1, 3, 5, 7, 13, 15, 17, 19]
    

    training_fishes = [Fish.randomFishGenerator(origin, "training") for i in range(10)]

    scores = []
    for i in training_fishes:
        fishes = []
        for j in range(0, 10):
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            loc = (possibleX[x], possibleY[y])
            f = Fish.randomFishGenerator(loc, "npc")
            fishes.append(f)
        i.score = 100
        fishes.append(i)
        aquarium = Aquarium(20, fishes)
        while aquarium.lifetime < 100 and fishes[-1].status == 1:
            aquarium.updateSim()
            print(aquarium)

        scores.append(i.score)
    print(scores)

    print("Run Demo:\n")

