from aquarium import Aquarium
from fish import Fish

if __name__ == '__main__':
    print("Running Main")
    fishes = []
    f = Fish((0,5), 5, 1, 0)
    fishes.append(f)
    aquarium = Aquarium(6, fishes)

    for i in range(0,5):
        aquarium.updateSim()
        print(aquarium)


    
