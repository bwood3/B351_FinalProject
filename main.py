from aquarium import Aquarium
from fish import Fish

if __name__ == '__main__':
    print("Running Main")
    fishes = []
    f = Fish((0,5))
    fishes.append(f)
    aquarium = Aquarium(5, fishes)
    print(aquarium)

    f = Fish((0,5))
    f.updateLoc((1, 1))
    print(f.NORTHEAST)
    
