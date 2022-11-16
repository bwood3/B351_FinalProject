from aquarium import Aquarium
from fish import Fish
import random
if __name__ == '__main__':
    print("Running Main")
    origin = (10, 10)  # starting point for the training fish
    fishes = []
    possibleX = [0, 2, 4, 6, 8, 12, 14, 16, 18, 20]
    possibleY = [0, 2, 4, 6, 8, 12, 14, 16, 18, 20]
    for i in range(0, 10):
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        loc = (possibleX[x], possibleY[y])
        f = Fish.randomFishGenerator(loc)
        fishes.append(f)
    aquarium1 = Aquarium(20, fishes)

    training_fishes = [Fish.randomFishGenerator(origin) for i in range(10)]

    print("Run Demo:\n")
    print("Fish origin: ", (10, 10))



