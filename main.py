from aquarium import Aquarium
from fish import Fish
import random
if __name__ == '__main__':
    print("Running Main")
    origin = (10, 10)  # starting point for the training fish
    fishes = []
    possibleX = [1, 3, 5, 7, 13, 15, 17, 19]
    possibleY = [1, 3, 5, 7, 13, 15, 17, 19]
    for i in range(0, 10):
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        loc = (possibleX[x], possibleY[y])
        f = Fish.randomFishGenerator(loc)
        fishes.append(f)
    aquarium1 = Aquarium(20, fishes)

    training_fishes = [Fish.randomFishGenerator(origin) for i in range(10)]

    print("Run Demo:\n")
    print("Fish origin: ", (10, 10))



