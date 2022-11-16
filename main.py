from aquarium import Aquarium
from fish import Fish

if __name__ == '__main__':
    print("Running Main")
    fishes = []
    origin = (0,5)
    print("Run Demo:\n")
    print("Fish origin: ",(0,5))

    f = Fish(origin, 5, 1, 0)
    fishes.append(f)
    aquarium = Aquarium(6, fishes)

    for i in range(1, 10):
        f = Fish.randomFishGenerator(origin)
        print(str(f.vision) + ", " + str(f.speed) + ", " + str(f.riskAwareness))


    
